class GameMap:
    def __init__(self):
        # Mapa: 0 = suelo transitable, 1 = pared/obstáculo
        self.map_data = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,1,0,0,0,1,1,1,1,1,1,0,0,0,1,1,0,1],
            [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
            [1,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,1],
            [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1],
            [1,0,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,0,1],
            [1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ]
        self.tile_size = 32
    
    def draw(self, canvas):
        """Dibuja el mapa en el canvas"""
        canvas.delete("map")
        
        for y, row in enumerate(self.map_data):
            for x, tile in enumerate(row):
                x1 = x * self.tile_size
                y1 = y * self.tile_size
                x2 = x1 + self.tile_size
                y2 = y1 + self.tile_size
                
                if tile == 1:  # Pared
                    canvas.create_rectangle(x1, y1, x2, y2, 
                                          fill="#654321", outline="#4A3018", 
                                          tags="map")
                else:  # Suelo
                    canvas.create_rectangle(x1, y1, x2, y2, 
                                          fill="#90EE90", outline="#7CCD7C", 
                                          tags="map")