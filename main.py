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

        result = segment_camera.segmentFrame(frame, show_bboxes=True, segment_target_classes=target_class)
        # Подсчитайте количество экземпляров объекта "человек" на кадре
        num_persons = len(result[0]["scores"])

        total_frames += 1
        if num_persons > 0:
            person_frames += 1

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()

    # Вычисление процента времени, когда был обнаружен человек
    percentage_time = (person_frames / total_frames) * 100
    print(f"Процент времени, когда зона была заполнена: {percentage_time}%")


def main():
    object_detection_on_a_image()


if __name__ == '__main__':
    main()