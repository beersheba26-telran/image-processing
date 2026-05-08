
import math
import pandas as pd
from ultralytics import YOLO
class ImageInfo:
    def __init__(self, path):
        """
        creating model from file "yolo8m-seg.pt"
        making required structure for optimal implementation below methods

        Args:
            path (str): Path to the image file.
        """
        
        model = YOLO('yolov8m-seg.pt')
        self.__allNames = model.names
        self.__boxes = model(path)[0].boxes
        self.__classIndices: dict[str, list[int]] = self.__getClassIndicesDict()
    def __getClassIndicesDict(self) -> dict[str, list[int]]:
        """
        Creates a dictionary that maps class names to lists of bounding box indices.

        Returns:
            dict[str, list[int]]: A dictionary where keys are class names and values are lists of bounding box indices.
        """
        res: dict[str, list[int]] = {}
        [self.__updateClassIndices(bi, box, res) for bi, box in enumerate(self.__boxes)] 
        return res 
    def __getDataFrame(self):
       
        xywhn = self.__boxes.xywhn.cpu().numpy()
        cls = self.__boxes.cls.cpu().numpy()
        conf = self.__boxes.conf.cpu().numpy()
        names = [self.__allNames[c] for c in cls]
        df = pd.DataFrame(xywhn[:,2:4], columns=['normalized width', 'normalized height'])
        df["class"] = names
        df["confidence"] = conf 
        return df    
        
    def __updateClassIndices(self, bi: int, box, res: dict[str, list[int]]):
        """Updates the class indices dictionary with the given bounding box information.
        Args:
            boxIndex (int): The index of the bounding box.
            box: The bounding box object.
            res (dict[str, list[int]]): The dictionary to update.
        """
        className: str = self.__allNames[box.cls.item()]
        res.setdefault(className, []).append(bi)
    def classBoxes(self, className:str) -> list[int] :
        """
        Returns a list of indices of bounding boxes for the specified class name.

        Args:
            className (str): The name of the class to filter bounding boxes.

        Returns:
            list[int]: A list of bounding boxes for the specified class.
        """ 
        return self.__classIndices.get(className, [])
    def boxInfo(self, boxIndex:int) -> tuple:
        """
        Returns tuble containing normalized center coordinates, confidence score

        Args:
            boxIndex (int): The index of the bounding box to retrieve information for.

        Returns:
           Returns tuble containing normalized center coordinates, confidence score
        """   
        box = self.__boxes[boxIndex]
        #using xywhn format to get the center coordinates and width and height of the bounding box
        x_center, y_center, *_ = box.xywhn[0].cpu().numpy()
        confidence = box.conf.item()
        return x_center, y_center,confidence
    def csvInfo(self, csvPath:str) -> None:
        """
        Saves the bounding box information to a CSV file.
        Each row of the CSV file contains the class name, confidence score, normalized width, and normalized height of a bounding box.
        Args:
            csvPath (str): The path where the CSV file will be saved.
        """    
        
        if not hasattr(self, "__df"):
            self.__df = self.__getDataFrame()
        self.__df.to_csv(csvPath, index=False)
    def __getDistanceBetween(self,boxInd1: int, boxInd2: int)->float :
        x1_center, y1_center, *_ = self.__boxes[boxInd1].xywhn[0].tolist()
        x2_center, y2_center, *_ = self.__boxes[boxInd2].xywhn[0].tolist()
        return math.hypot(x1_center - x2_center, y1_center - y2_center)
    def __getMinDistance(self, boxIndex: int, boxIndices: list[int]) -> tuple[int, float]:
        res: tuple[int, float] = (boxIndices[0], self.__getDistanceBetween(boxIndex, boxIndices[0] ))
        for bi in boxIndices:
            if (d := self.__getDistanceBetween(boxIndex, bi)) < res[1]:
                res = (bi, d)
        return res        
    def __getBagsPersonDict(self):
        bagsIndices = self.classBoxes("suitcase") + self.classBoxes("handbag") + \
        self.classBoxes("backpack")
        personIndices = self.classBoxes("person")
        res: dict[int, tuple[int, float]] = {bi: self.__getMinDistance(bi, personIndices)
                                             for bi in bagsIndices}
        return res
    def bagsPersons(self, threshold:float) -> dict:
        """
        Returns a dictionary containing index of bounding boxes for handbags, suitcases as key and tuple as value, where the tuple contains the index of bounding box for person and relative distance
        from bounding box of the handbag/suitcase/bag and person box.
        Nearest person to the handbag/suitcase
        In the case no person is detected within the specified threshold distance, the value for that bag will be None. 
        Args:
            threshold (float): The distance threshold to consider for associating handbags/suitcases with persons.
        
        """   
        if not hasattr(self, "__bagPerson"):
            self.__bagPerson: dict[int, tuple[int, float]] = self.__getBagsPersonDict()
        belongPerson: dict[int, tuple[int, float]] = \
        {bi: (pi,d) for bi, (pi, d) in self.__bagPerson.items()
         if d <= threshold} 
        noBelongPerson:dict[int, None] = \
            {bi: None for bi, (_, d) in self.__bagPerson.items() 
             if d > threshold}
        return belongPerson | noBelongPerson     