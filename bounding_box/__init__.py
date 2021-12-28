import cv2
import matplotlib.pyplot as plt

def bounding_box():
  image = cv2.imread("Pratapgarh/IMAGE/307095_Pratapgarh_01_04.png")
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  blurred = cv2.GaussianBlur(gray, (5, 5), 0)

  canny = cv2.Canny(blurred, 30, 300)
  (cnts, _) = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

  coins = image.copy()

  cv2.drawContours(coins, cnts, -1, (255, 0, 0), 2)

  for cnt in cnts:
    x, y, w, h = cv2.boundingRect(cnt)
    cv2.rectangle(coins, (x, y), (x + w, y + h), (0, 255, 0), 2)

  # Routine to fix
  def fixColor(image):
    return (cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

  output_img = (fixColor(coins)
  cv2.imshow('Output Image', output)