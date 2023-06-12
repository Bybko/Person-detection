import cv2
from pixellib.instance import instance_segmentation


def object_detection_on_a_image():
    segment_camera = instance_segmentation(infer_speed="rapid")
    segment_camera.load_model("mask_rcnn_coco.h5")

    target_class = segment_camera.select_target_classes(person=True)
    camera = cv2.VideoCapture(0)

    total_frames = 0
    person_frames = 0

    while True:
        success, frame = camera.read()

        if not success:
            break

        roi = frame[100:400, 200:500]
        result = segment_camera.segmentFrame(roi, show_bboxes=True, segment_target_classes=target_class)

        num_persons = len(result[0]["scores"])

        total_frames += 1
        if num_persons > 0:
            person_frames += 1

        cv2.rectangle(frame, (200, 100), (500, 400), (0, 255, 0), 2)
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()

    percentage_time = (person_frames / total_frames) * 100
    print(f"Процент времени, когда зона была заполнена: {percentage_time}%")


def main():
    object_detection_on_a_image()


if __name__ == '__main__':
    main()