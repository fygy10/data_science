
#MAIN SCRIPT
#Parent class init function and __repr__ in case it is called on its own for whatever reason
class Student:

    def __init__(self, student_id, major, university):
        self.student_id = student_id
        self.major = major
        self.university = university


    def __repr__(self):
        return f'Student ID: {self.student_id}, Major: {self.major}, University: {self.university}'
    

class Project(Student):
    
    #init function for the subclass
    def __init__(self, student_id, major, university, project_id, data_points=None):
        super().__init__(student_id, major, university)
        if not isinstance(project_id, int):
            print('The project id must be an integer.')
        self.project_id = project_id
        self.data_points = data_points or []    #carrying data through the code to be processed
        self.__analysis_results = {}    #storing the results of each instance passed through the code (private)
        self.__active = True    #default set to True (private)


    #adds new data to the data points list
    #checks if it is the correct (numerical) type of data first 
    def add_data(self, new_data):
        if not isinstance(new_data, (int , float)):
            print('The new data must be numerical')
        self.data_points.append(new_data)


    #returns analysis results dictionary
    def get_results(self):
        return self.__analysis_results


    #returns status of the active attribute
    def is_active(self):
        return self.__active


    #sets active status to true or false
    def set_active(self, status):
        if isinstance(status, bool):
            self.__active = status
            return self.__active
        else:
            print('This is not a boolean value status')
        

    #analyze data points to update/store analysis_results with statistical (mean, median, and variance)
    #operations are seperate methods for readability and modularity
    #cannot use built in functions for statistical analysis
    #use sample formula to calculate variance
    #allows for call at the instance level and not inside the class
    def perform_analysis(self):

        #handles empty list of data points
        if self.data_points == None:
            print('There are not data points to perform an analysis.')
            return
        
        #adds results to the dictionary; call on the individual operation methods below
        try:

            self.__analysis_results['mean'] = self.mean_datapoints()
            self.__analysis_results['median'] = self.median_datapoints()
            self.__analysis_results['variance'] = self.variance_datapoints()

        #second check on numerical data and math operation error for division by zero
        except TypeError:
            print("The new data must be numerical.")
        except ZeroDivisionError:
            print("The was an attmept of division by zero that occurred; check your data points.")


    #calculates the mean of the data points
    def mean_datapoints(self):
        mean  = sum(self.data_points)/len(self.data_points)
        return mean
        

    #calculates the median of the data points
    #if, else statements handle the even and odd cases of the length of the data points
    def median_datapoints(self):
        self.data_points = sorted(self.data_points)
        length = len(self.data_points)
        if length % 2 == 0:
            median = (self.data_points[length // 2 - 1] + self.data_points[length // 2]) / 2
        else:
            median = self.data_points[length // 2]
        return median 


    #calculates the variance (sample) of the data points
    def variance_datapoints(self):
        if len(self.data_points) >= 1:
            mean = self.mean_datapoints()
            len_data = len(self.data_points)
            variance_sum = sum((x - mean) ** 2 for x in self.data_points)
            return variance_sum / (len_data - 1) if len_data > 1 else 0
        



#TESTS FOR THE SCRIPT
#test case to check if the method catches the non-numerical value being passed through
import unittest


class Test(unittest.TestCase):

    def test_exceptions(self):

        project = Project(student_id=1000, major="Computer Science", university="Harvard", project_id=1)
        project.data_points = [10, 20, 'abc']
        project.perform_analysis()

unittest.main(argv=[''], exit=False)



#test case to check if the data points is None when empty and perform analsysis

class Test(unittest.TestCase):

    def test_validate(self):

        project = Project(student_id=1000, major="Computer Science", university="Harvard", project_id=1)
        project.data_points = []
        result = project.perform_analysis()
        self.assertFalse(None, result)

unittest.main(argv=[''], exit=False)



test1 = [(1000, 'Computer Science', 'HARVARD', 1, [65,75,95,99]),(1001, 'Computer Science', 'MIT', 2, [95,35,75,90,91]),\
         (1003,'Data Science', 'Cornell', 3, [75,85,95,99,33])]


for test in test1:
    project = Project(test[0],test[1],test[2],test[3],test[4])
    project.perform_analysis()
    project_info = f"Student id : {project.student_id}\nMajor: {project.major}\nUniversity:{project.university}\n\
project_id:{project.project_id}\ndata_points : {project.data_points}\nis_active:{project.is_active()}"
    print(project_info)
    print(f"analysis results :{project.get_results()}\n")



test = (1000, 'Computer Science', 'HARVARD', 1, [65,75,95,99])
project = Project(test[0],test[1],test[2],test[3],test[4])
project.perform_analysis()
print(f"analysis results before : {project.get_results()}")
project.add_data(22)
project.perform_analysis()
print(f"analysis results after: {project.get_results()}")