
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from ortools.sat.python import cp_model

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class QueensSolver:
    def __init__(self, url):
        self.game_url = url
        self.grid_data = None
        self.grid_elements = None
        
        self.result = None
        
    def execute_linkedin(self):
        self._get_data_linkedin()
        result = self._solve_cp()
        self.input_solution(result)
        self.input_solution(result)
        
        
    def execute(self):
        self._get_data()
        result = self._solve_cp()
        if result:
            self.input_solution(result)
        else:
            print("no result...")
            
    def log_in_linkedin(self):
        # Path to your chromedriver
        chrome_options = Options()
        # Initialize driver
        self.driver = webdriver.Chrome(options=chrome_options)
        # Open LinkedIn
        self.driver.get("https://www.linkedin.com")
            
            
    def _get_data_linkedin(self):
        self.driver.get("https://www.linkedin.com/games/queens")
        board_xpath = '/html/body/div[7]/div[3]/div/div[1]/div[2]/div/div/main/div/div[1]/section'
        board = self.driver.find_element(By.XPATH, board_xpath)
        # Only immediate children (the cells)
        cells = board.find_elements("css selector", ".queens-cell-with-border")
            
        size = int(len(cells)**0.5)
        
        grid_data = {}
        grid_elements = {}
        # Find all game cells on the page
        for i, cell in enumerate(cells):
            x = i % size
            y = i // size
            classes = cell.get_attribute("class").split()
            color_class = [c for c in classes if c.startswith("cell-color-")]
            color_id = int(color_class[0].split("-")[-1]) if color_class else 0
            # Use a string key "x,y" to represent the cell's position
            grid_data[(x, y)] = color_id
            grid_elements [(x, y)] = cell
        
        self.grid_data = grid_data
        self.grid_elements = grid_elements
    

    def _get_data(self):
        # Set up Chrome options
        chrome_options = Options()
        
        # Initialize the Chrome driver.
        self.driver = webdriver.Chrome(options=chrome_options)
        
        # Open a URL to test that the browser opens
        self.driver.get(self.game_url)
        
        grid_data = {}
        grid_elements = {}
        # Find all game cells on the page
        cells = self.driver.find_element(By.XPATH, "//*[@id='grid']")
        for row in cells.find_elements(By.XPATH, "./*"):
            for col in row.find_elements(By.XPATH, "./*"):
                x, y = [int(val) for val in col.get_attribute("id").split("-")[1:]]
                region = col.get_attribute("style")
            
                # Use a string key "x,y" to represent the cell's position
                grid_data[(x, y)] = region
                grid_elements [(x, y)] = col
        
        self.grid_data = grid_data
        self.grid_elements = grid_elements

    def _solve_cp(self):
        model = cp_model.CpModel()
        solver = cp_model.CpSolver()
        
        # Create variables: 1 if queen is placed at (x,y), else 0
        queens = {(x, y): model.NewBoolVar(f'queen_{x}_{y}') for (x, y) in self.grid_data.keys()}
        
        # Extract regions, rows, and columns
        regions = {}
        rows = {}
        cols = {}
        for (x, y), region in self.grid_data.items():
            regions.setdefault(region, []).append(queens[(x, y)])
            rows.setdefault(x, []).append(queens[(x, y)])
            cols.setdefault(y, []).append(queens[(x, y)])
        
        # Constraints
        # 1. Exactly one queen per region
        for region in regions.values():
            model.AddExactlyOne(region)
        
        # 2. At most one queen per row and column
        for row in rows.values():
            model.AddAtMostOne(row)
        for col in cols.values():
            model.AddAtMostOne(col)
        
        # 3. No adjacent queens (including diagonally)
        for (x1, y1), var1 in queens.items():
            for (x2, y2), var2 in queens.items():
                if (x1, y1) != (x2, y2) and abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1:
                    model.AddAtMostOne([var1, var2])
        
        # Solve and return solution
        status = solver.Solve(model)
        if status == cp_model.OPTIMAL:
            return [(x, y) for (x, y), var in queens.items() if solver.Value(var) == 1]
        else:
            return None
        
    def input_solution(self, result):
        for key in result:
            self.grid_elements[key].click()
            
            
if __name__ == "__main__":
    
    game_url = "https://www.queens-game.com/?map=map66"
    queens = QueensSolver(game_url)
    queens.execute()
    
    queens = QueensSolver("")
    queens.log_in_linkedin()
    queens.execute_linkedin()
    
