from __future__ import annotations
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
from sobel import sobell, to_gray
import cv2
class CriminisiInpainting:
    def __init__(self, image: np.ndarray, mask: np.ndarray, patch_size: int = 9):
        self.img = image.astype(np.float64)/255.0  # Normalize image to [0, 1]
        self.mask = mask.astype(bool)
        self.ps = patch_size
        self.half = patch_size // 2
        h, w = self.mask.shape
        self.img[self.mask] = 0.0
        self.unknow = self.mask.copy()
        self.conf = (~self.mask).astype(np.float64)
        wins = np.moveaxis(sliding_window_view(self.img, (self.ps, self.ps),axis=(0, 1)), 2,-1)
        windows_mask = sliding_window_view(self.mask, (self.ps, self.ps))
        valid = ~windows_mask.any(axis=(2, 3))
        self._cand = np.ascontiguousarray(wins[valid])

    def _get_front(self):
        kernel = np.ones((3, 3), dtype=np.uint8)
        dilated = cv2.dilate(self.unknow.astype(np.uint8), kernel)
        front = self.unknow & (dilated.astype(bool))
        return np.argwhere(front)
    def step(self):
        coords = self._get_front()
        gray = to_gray(self.img)
        gray = np.where(self.unknow, 0.0, gray)
        s = sobell(gray)
        karnel = np.ones((3, 3), dtype=np.uint8)
        valid_grad = ~cv2.dilate(self.unknow.astype(np.uint8), karnel).astype(bool)
        gx = np.where(valid_grad, s.gx/8.0, 0.0)
        gy = np.where(valid_grad, s.gy/8.0, 0.0)
        gmag = np.hypot(gx, gy)
        sm = sobell(self.unknow.astype(np.float64))
        nm = np.hypot(sm.gx, sm.gy)
        nx, ny = sm.gx/np.maximum(nm,1.0), sm.gy/np.maximum(nm,1.0)
        best_p, best_idx = -1,0
        best_path_info = None
        for idx, (r, c) in enumerate(coords):
            r0 = min(max(r - self.half, 0), self.img.shape[0] - self.ps)
            c0 = min(max(c - self.half, 0), self.img.shape[1] - self.ps)
            sl = (slice(r0, r0 + self.ps), slice(c0, c0 + self.ps))

            # Pewność (C)
            C = self.conf[sl].sum() / (self.ps * self.ps)
            
            # Dane strukturalne (D) - dopasowanie izofoty do normalnej
            m = gmag[sl] * (~self.unknow[sl])
            if m.max() > 0:
                max_k = np.argmax(m)
                gxx, gyy = gx[sl].flat[max_k], gy[sl].flat[max_k]
                D = abs(-gyy * nx[r, c] + gxx * ny[r, c])
            else:
                D = 1e-3

            priority = C * (D + 1e-3)
            if priority > best_p:
                best_p = priority
                best_idx = idx
                best_patch_info = (r0, c0, sl, C)
        r, c = coords[best_idx]
        r0, c0, sl, C = best_patch_info

        target = self.img[sl]
        known = ~self.unknow[sl]
        diff = self._cand - target[None]
        ssd = ((diff ** 2).sum(axis=3) * known[None]).sum(axis=(1, 2))
        best_cand_idx = np.argmin(ssd)
        unk = self.unknow[sl]
        self.img[sl][unk] = self._cand[best_cand_idx][unk]
        self.conf[sl][unk] = C
        self.unknow[sl] = False
        return True
    def run(self):
        while self.unknow.any():
            success = self.step()
            if not success:
                break
        
        # Zwrócenie wynikowego obrazu w skali 0-255
        out = self.img[..., 0] if self.img.shape[2] == 1 else self.img
        return np.clip(out * 255.0, 0, 255).astype(np.uint8)

def inpaint(image, mask, patch_size: int = 9):
    return CriminisiInpainting(image, mask, patch_size).run()