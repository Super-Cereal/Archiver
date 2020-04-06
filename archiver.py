import os
import sys
import time
import numpy as np
import shutil
from data.archiver_add import Ui_Interface
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox


def HRF(size):
    # human read format :)
    for elem in ["Б", "КБ", "МБ", "ГБ"]:
        if size // 1024 > 0:
            size = size / 1024
        else:
            break
    return str(round(size)) + elem


def get_structed_folder(path):
    resnp = np.array(path.split('\\')[-1])
    files = np.array(range(0))
    x = '     '
    for elem in os.listdir(path):
        npath = os.path.join(path, elem)
        if os.path.isdir(npath):
            count_dir = count_files = 0
            for elem2 in os.listdir(npath):
                if os.path.isdir(os.path.join(npath, elem2)):
                    count_dir += 1
                else:
                    count_files += 1
            resnp = np.append(resnp, x * 1 + elem)
            resnp = np.append(resnp, [x * 2 + f'{count_dir} папок.', x * 2 + f'{count_files} файлов.'])
        else:
            files = np.append(files, x * 1 + elem + x * 2 + HRF(os.path.getsize(npath)))
    return np.append(resnp, files)


class Interface(QMainWindow, Ui_Interface):
    def __init__(self):
        super().__init__()
        super().setupUi(self)

    def copy(self):
        from_path, to_path = self.from_path.text().replace('/', '\\'), self.to_path.text().replace('/', '\\')
        if not os.path.exists(from_path):
            QMessageBox.about(self, 'Error', 'Такого пути не существует!')
        else:
            try:
                if not os.path.exists(to_path):
                    os.makedirs(to_path)
                root_dir, base_dir = os.path.split(from_path)
                base_name = f'{root_dir}\\{"_".join("_".join(time.ctime().split()).split(":"))}'
                name = shutil.make_archive(base_name, "zip", root_dir, base_dir)
                try:
                    shutil.move(name, to_path)
                except shutil.Error:
                    pass
                QMessageBox.about(self, 'Correct', 'Копирование завершено!')
            except Exception:
                QMessageBox.about(self, 'Error', 'Неожиданная ошибка!')

    def reset(self):
        self.from_path.clear()
        self.to_path.clear()
        self.textBrowser.setText('None')

    def update_text(self):
        from_path = self.from_path.text()
        if os.path.exists(from_path):
            self.textBrowser.setText('\n'.join(get_structed_folder(from_path)))
        else:
            self.textBrowser.setText('None')


def main():
    app = QApplication(sys.argv)
    interface = Interface()
    interface.show()
    app.exec()


if __name__ == "__main__":
    main()
