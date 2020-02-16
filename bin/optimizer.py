from Scanner import ROOT_DIR

data = ROOT_DIR + "/env/data/"

class Memory:
    def __init__(self, project, view, sensor_id):
        self.project = project
        self.view = view
        self.sensor_id = sensor_id

    def stage_out(self):
        # write out key with project,view, and ID for future runs
        # append y,z to array x
        sensor_ids += self.sensor_id
        pass

    def write_out(self):
        # On run end, rewrite line in storage file
        print(staged_ID, data+self.project+'.txt')
        pass

class Recall:
    def __init__(self):
        Imporxt = data+self.project
