from core import Model, Camera


def main():
    model = Model('mask_rcnn_coco.h5', infer_speed='average', person=True)
    camera = Camera(model)
    camera.start()


if __name__ == '__main__':
    main()

