import os
import os.path



class FileOps():
    def __init__(self, base_path=None, data_path=None):
        if base_path:
            self.path = fr'{os.path.abspath(base_path)}'
        else:
            self.path = fr'{os.getcwd()}'
            
        if data_path:
            self.path = fr'{self.path}\{data_path}'
            
        
        if not os.path.exists(self.path):
            raise FileNotFoundError(self.path, " non-existent")

    def is_file(self, file):
        if isinstance(file, list):
            for x in file:
                ret = os.path.isfile(fr'{self.path}\{file}')
                
                if not ret:
                    return False
                    
        else:
            ret = os.path.isfile(fr'{self.path}\{file}')
            
        return ret

    def is_dir(self, file):
        if isinstance(file, list):
            for x in file:
                ret = os.path.isdir(fr'{self.path}\{file}')
                
                if not ret:
                    return False
                    
        else:
            ret = os.path.isdir(fr'{self.path}\{file}')
            
        return ret

    def is_rw(self, file):
        if isinstance(file, list):
            for x in file:
                ret = os.access(fr'{self.path}{file}', os.R_OK & os.W_OK)
                
                if not ret:
                    return False
                    
        else:
            ret = os.access(fr'{self.path}\{file}', os.R_OK & os.W_OK)
            
        return ret

    def touch(self, file):
        if self.is_file(file):
            print(fr'WARNING: Could not create file "{self.path}\{file}". File exists.')
            return False

        fd = open(fr'{self.path}\{file}', "x")
        fd.close()

        return True
        
    def mkdir(self, file):
        if self.is_dir(file):
            print(fr'ALERT: Did not create directory: "{self.path}\{file}". Directory exists.')
            return False
        else:
            os.mkdir(fr'{self.path}\{file}')
        
        return True

    def rename(self, old, new):
            os.rename(fr'{self.path}\{old}', fr'{self.path}\{new}')

    def delete(self, file):
        if self.is_file(file):
            os.remove(fr'{self.path}\{file}')
        elif self.is_dir(file):
            os.rmdir(fr'{self.path}\{file}')
        else:
            raise Exception(fr'FileError: Unknown file operation error: "{self.path}\{file}')



base = fr'C:\Users\rootp\Documents\Code\Python\GUI\PyPad'
data = fr'userData\Categories\test'

fo = FileOps(base, data)

#fo.touch("touch.txt")
#fo.mkdir("dir_test")

#print(fo.is_file("touch.txt"))
#print(fo.is_dir("dir_test"))
#print(fo.is_rw("touch.txt"))

#fo.rename("touch.txt", "touched.txt")
#fo.rename("dir_test", "dir_tested")

fo.delete("touched.txt")
fo.delete("dir_tested")



#print("Debugged, but needs a final testing later...")
