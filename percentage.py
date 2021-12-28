import pixellib
from pixellib.semantic import semantic_segmentation
import cv2 as cv
import numpy as np
import streamlit as st
import os
import SessionState


def app(session_state):
    if session_state.login_state:
        st.title("Visualization II")
        pwd = os.getcwd()
        segment_image = semantic_segmentation()
        net = segment_image.load_pascalvoc_model(os.path.join("Pratapgarh/models"
                                                              "/deeplabv3_xception_tf_dim_ordering_tf_kernels.h5"))
        seg_image = segment_image.segmentAsPascalvoc(os.path.join("307095_Pratapgarh_01_03.png"),
                                                     output_image_name=os.path.join("out.png"))

        overlay_img = segment_image.segmentAsPascalvoc(os.path.join("307095_Pratapgarh_01_03.png"),
                                                       output_image_name=os.path.join("out1.png"), overlay=True)

        image = cv.imread(os.path.join("out.png"))
        image_2 = cv.imread(os.path.join("out1.png"))
        final_frame = cv.hconcat((image, image_2))
        orignal = cv.imread(os.path.join("307095_Pratapgarh_01_03.png"))

        st.write("Original Plot")

        st.image(orignal)

        st.write("Plot After Segmentation")
        st.image(final_frame)
        # import cv2
        # cv2.imshow('Original plot',orignal)
        # cv2.waitKey(0)
        # cv2.imshow('Plot after Segmentation ',final_frame)
        # cv2.waitKey(0)
        # print('\n')

        pic_arr = np.asarray(image)
        # pic_arr.shape
        img = cv.imread(os.path.join("out.png"))
        img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

        sensitivity = 20
        lower_bound = np.array([0, 120, 70])
        upper_bound = np.array([10, 255, 255])
        # create mask
        msk = cv.inRange(img_hsv, lower_bound, upper_bound)

        st.write("Mask")
        st.image(msk)

        # import cv2
        # cv2.imshow('',msk)
        # cv2.waitKey(0)

        def calcPercentage(self, msk):
            height, width = msk.shape[:2]
            num_pixels = height * width
            count_white = cv.countNonZero(msk)
            percent_white = (count_white / num_pixels) * 100
            percent_white = round(percent_white, 2)
            return percent_white

        perc = calcPercentage(img_hsv, msk)
        st.write("White % = " + str(perc))
        st.write("Black % = " + str(100 - perc))

    else:
        st.write("please login first")
