import numpy as np
import cv2

def rotate_image(image, angle, center=None, border_mode=cv2.BORDER_CONSTANT):
    """
    Rotate the image by angle degrees.
    image: BGR numpy array
    """
    h, w = image.shape[:2]
    if center is None:
        center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=border_mode, borderValue=(255,255,255))
    return rotated

def scale_image(image, scale_factor):
    h, w = image.shape[:2]
    new_w = max(1, int(w * scale_factor))
    new_h = max(1, int(h * scale_factor))
    scaled = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
    # pad or crop back to original size for consistent display
    canvas = np.ones((h, w, 3), dtype=np.uint8) * 255
    y = (h - new_h) // 2
    x = (w - new_w) // 2
    if new_h <= h and new_w <= w:
        canvas[y:y+new_h, x:x+new_w] = scaled
    else:
        # crop scaled to fit
        canvas = scaled[0:h, 0:w]
    return canvas

def translate_image(image, tx, ty):
    h, w = image.shape[:2]
    M = np.float32([[1, 0, tx], [0, 1, ty]])
    translated = cv2.warpAffine(image, M, (w, h), borderMode=cv2.BORDER_CONSTANT, borderValue=(255,255,255))
    return translated

def shear_image(image, shear_x=0.0, shear_y=0.0):
    """
    Apply shear along x and/or y. shear_x, shear_y are factors.
    """
    h, w = image.shape[:2]
    M = np.array([[1, shear_x, 0],
                  [shear_y, 1, 0]], dtype=np.float32)
    # compute new bounds to keep image within view
    new_w = int(w + abs(shear_x) * h)
    new_h = int(h + abs(shear_y) * w)
    sheared = cv2.warpAffine(image, M, (w, h), borderMode=cv2.BORDER_CONSTANT, borderValue=(255,255,255))
    return sheared

def flip_image(image, mode=1):
    """
    mode: 1 horizontal, 0 vertical, -1 both
    """
    flipped = cv2.flip(image, mode)
    return flipped

def apply_convolution(image, kernel, normalize=True):
    """
    Apply kernel to image. If image is color, apply to each channel.
    kernel: numpy 2D array
    normalize: if True and kernel sum != 0, normalize kernel to sum 1
    """
    k = np.array(kernel, dtype=np.float32)
    s = np.sum(k)
    if normalize and abs(s) > 1e-6:
        k = k / s
    # handle grayscale or color
    if len(image.shape) == 2 or image.shape[2] == 1:
        result = cv2.filter2D(image, -1, k, borderType=cv2.BORDER_REPLICATE)
        return result
    else:
        channels = []
        for c in range(3):
            ch = cv2.filter2D(image[:, :, c], -1, k, borderType=cv2.BORDER_REPLICATE)
            channels.append(ch)
        merged = cv2.merge(channels)
        # clip and convert
        merged = np.clip(merged, 0, 255).astype(np.uint8)
        return merged

def predefined_kernels():
    """
    Returns a dictionary of common kernels.
    """
    return {
        "blur_3": np.ones((3,3), dtype=np.float32),
        "gaussian_5": cv2.getGaussianKernel(5, -1) @ cv2.getGaussianKernel(5, -1).T,
        "sharpen": np.array([[0,-1,0], [-1,5,-1], [0,-1,0]], dtype=np.float32),
        "edge_sobel_x": np.array([[-1,0,1], [-2,0,2], [-1,0,1]], dtype=np.float32),
        "edge_sobel_y": np.array([[-1,-2,-1], [0,0,0], [1,2,1]], dtype=np.float32),
        "laplacian": np.array([[0,1,0], [1,-4,1], [0,1,0]], dtype=np.float32),
    }

