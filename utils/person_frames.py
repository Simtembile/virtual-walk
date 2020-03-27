from utils.person import Person
import numpy as np
import math

class PersonMovement:
    def __init__(self, list_persons, times_v=10):
        self.list_persons = list_persons
        self.n_frames = len(list_persons)
        self.coords = self.get_vector(times_v)

    def get_vector(self, times_v):
        v = []

        xs = np.array([person.keypoints_positions for person in self.list_persons])
        hs = np.array([person.H for person in self.list_persons])

        for i_person in range(1, self.n_frames):
            vix = (self.list_persons[i_person].keypoints[17].x - self.list_persons[i_person - 1].keypoints[17].x) ** 2
            viy = (self.list_persons[i_person].keypoints[17].y - self.list_persons[i_person - 1].keypoints[17].y) ** 2
            v.append(math.sqrt(vix + viy))

        avg_h = np.mean(hs)
        x = (xs - np.mean(xs)) / avg_h
        v = np.array(v / avg_h)
        v_joints = np.empty((self.n_frames - 1, x.shape[1], x.shape[2]))
        for i_person in range(xs.shape[0] - 1):
            v_joints[i_person,:] = x[i_person + 1, :] - x[i_person, :]

        coords = np.concatenate((xs.flatten(), np.repeat(v.flatten(), times_v), v_joints.flatten()))
        coords = np.reshape(coords, (1, coords.shape[0]))

        return coords

    def write_to_txt(self, path, label):
        writer = np.append([label], self.coords)
        np.savetxt(path, writer, delimiter='\t')


if __name__ == '__main__':
    path = '../prueba.txt'
    p = Person(path_txt=path)
    p2 = p
    list_p = [p, p, p, p, p]
    group = PersonMovement(list_p)
    c = group.get_vector(10)