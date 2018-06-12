import cv2


def get_image():
    camera = cv2.VideoCapture(0)
    return_value, image = camera.read()
    cv2.imwrite('opencv.png', image)
    del camera
    return image
