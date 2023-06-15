import cv2
from pixellib.instance import instance_segmentation

from core import Model, Camera


def object_detection_on_a_image():
    capture = cv2.VideoCapture(0)

    segment_video = instance_segmentation(infer_speed="rapid")
    segment_video.load_model("mask_rcnn_coco.h5")
    target_class = segment_video.select_target_classes(person=True)
    segment_video.process_camera(capture, segment_target_classes=target_class ,frames_per_second=15, show_frames=True,
                                 output_video_name="dayaebaletuhuety.mp4",frame_name="frame")

    total_frames = 0
    person_frames = 0

    percentage_time = (person_frames / total_frames) * 100
    print(f"Процент времени, когда зона была заполнена: {percentage_time}%")


def main():
    object_detection_on_a_image()
    # model = Model('mask_rcnn_coco.h5', person=True)
    # camera = Camera(model)
    # camera.start()


if __name__ == '__main__':
    main()

