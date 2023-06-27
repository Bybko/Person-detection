from application.desktop import DesktopApplication


def main():
    application = DesktopApplication(debug=True)
    application.start()
    application.stop()


if __name__ == '__main__':
    main()
