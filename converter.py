import cv2
import os
import sys
import numpy
import shutil
import time

DEFAULT_SRC_PATH = "D:\\BaiduNetdiskDownload\\Part K (羊羽忍)"
DEFAULT_QUALITY = 80
SUPPORT_LIST = [".jpg", ".jpeg", ".png"]
CONVERTED_PREFIX = "converted"
TEMP_FILE = "~\\tempfile_please_delete"

class Converter(object):
    
    def __init__(self, src_path):
        self.src = src_path
        self.qualities = [int(cv2.IMWRITE_JPEG_QUALITY), 90, int(cv2.IMWRITE_PNG_COMPRESSION), 4]

    def init(self):
        # if src path exists
        if not os.path.exists(self.src):
            return False

        self.filelist = []
        self.dirlist = []

        # if it is a folder
        if os.path.isdir(self.src):
            for parent, dir_names, file_names in os.walk(self.src):
                for dir_name in dir_names:
                    self.dirlist.append(os.path.join(parent,dir_name))
                for file_name in file_names:
                    if os.path.splitext(file_name)[-1] in SUPPORT_LIST:
                        self.filelist.append(os.path.join(parent,file_name))
                    else:
                        print("%s skipped, file type not supported"%(os.path.join(parent, file_name)))
        else:
            if os.path.splitext(self.src)[-1] in SUPPORT_LIST:
                self.filelist.append(self.src)
            else:
                print("%s skipped, file type not supported"%(self.src))

    def convert(self, quality = DEFAULT_QUALITY):
        # Create all the directories

        parent = os.path.dirname(self.src)
        basename = os.path.basename(self.src)
        basename = os.path.splitext(basename)[0]

        newpath = os.path.join(parent, "%s-%s"%(CONVERTED_PREFIX, basename))
        try:
            os.makedirs(newpath)
        except:
            pass

        for dir_name in self.dirlist:
            relpath = os.path.relpath(dir_name, parent)
            try:
                os.makedirs(os.path.join(newpath, relpath))
            except:
                pass

        for file_name in self.filelist:
            relpath = os.path.relpath(file_name, parent)

            # copy the file to temppath to convert because unicode path is not supported by opencv
            file_ext = os.path.splitext(file_name)[-1]
            temp_path = os.path.expanduser(TEMP_FILE + file_ext)
            shutil.copyfile(file_name, os.path.expanduser(temp_path))
            temp_path_converted = os.path.expanduser(TEMP_FILE + "-converted" + file_ext)

            # convert
            img = cv2.imread(temp_path)
            cv2.imwrite(temp_path_converted, img, self.qualities)

            #copy back
            shutil.copyfile(temp_path_converted, os.path.join(newpath, relpath))

            # delete the tempfile, explorer may opening the file, so wait for 1s if met a permission error
            try: 
                os.remove(temp_path)
            except PermissionError as pe:
                time.sleep(1)
                os.remove(temp_path)

            try: 
                os.remove(temp_path_converted)
            except PermissionError as pe:
                time.sleep(1)
                os.remove(temp_path_converted)

            print("Convertied %s"%(os.path.join(newpath, relpath)))
        
            

if __name__ == '__main__':
    converter = Converter(DEFAULT_SRC_PATH)
    converter.init()
    converter.convert()
