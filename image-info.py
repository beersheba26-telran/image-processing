class ImageInfo:
    def __init__(self, path):
       #TODO 
        """
        creating model from file "yolo8m-seg.pt"
        making required structure for optimal implementation below methods

        Args:
            path (str): Path to the image file.
        """
    def classBoxes(self, className:str) -> list[int] :
        #TODO 
        """
        Returns a list of indices of bounding boxes for the specified class name.

        Args:
            className (str): The name of the class to filter bounding boxes.

        Returns:
            list[int]: A list of bounding boxes for the specified class.
        """ 
    def boxInfo(self, boxIndex:int) -> tuple:
        #TODO 
        """
        Returns tuble containing normalized center coordinates, confidence score

        Args:
            boxIndex (int): The index of the bounding box to retrieve information for.

        Returns:
           Returns tuble containing normalized center coordinates, confidence score
        """     
    def csvInfo(self, csvPath:str) -> None:
        #TODO 
        """
        Saves the bounding box information to a CSV file.
        Each row of the CSV file contains the class name, confidence score, normalized width, and normalized height of a bounding box.
        Args:
            csvPath (str): The path where the CSV file will be saved.
        """    
    def bagsPersons(self, threshold:float) -> dict:
        #TODO 
        """
        Returns a dictionary containing index of bounding boxes for handbags, suitcases as key and tuple as value, where the tuple contains the index of bounding box for person and relative distance
        from bounding box of the handbag/suitcase/bag and person box.
        Nearest person to the handbag/suitcase
        In the case no person is detected within the specified threshold distance, the value for that bag will be None. 
        Args:
            threshold (float): The distance threshold to consider for associating handbags/suitcases with persons.
        
        """    