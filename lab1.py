import sys
import copy

DEF_COINS_NUM = 1000000
DEF_COINS_DIV = 1000
MAX_XY_VAL = 10
MIN_XY_VAL = 1

class city_coordinates:


    def __init__(self, x, y):
        self.x = x
        self.y = y



class city:


    def __init__(self, x, y, country_names: list, country_name = None):
        
        self.complete = 0    
        self.x = x
        self.y = y
        self.country_name = country_name
        self.coins = {}

        for cn in country_names:
            self.coins[cn] = DEF_COINS_NUM if cn == country_name else 0     

    def european(self):

        return self.country_name is not None


class country:


    def __init__(self, name, xl, yl, xh, yh):
        self.name = name
        self.xl = int(xl) - 1
        self.yl = int(yl) - 1
        self.xh = int(xh)
        self.yh = int(yh)
        self.complete = 0
        self.city_coordinates = []

    def check_input_data(name, xl, yl, xh, yh) -> bool:

        return False if (not (MIN_XY_VAL <= int(xl) <= int(xh) <= MAX_XY_VAL) or
                         not (MIN_XY_VAL <= int(yl) <= int(yh) <= MAX_XY_VAL)) else True
        
    def add_city(self, city):

        self.city_coordinates.append(city_coordinates(city.x, city.y))
    
    def show(self):

        print(f"{self.name}: {self.complete}")

    

class testcase_data:


    def __init__(self, num):
        self.num = num
        self.countries = []
        self.xl = sys.maxsize
        self.yl = sys.maxsize
        self.xh = 0
        self.yh = 0
        self.world = None
        self.iteration_count = 0
        self.complete = 0
        
    def add_coutry(self, c: country) -> bool:

        append_allowed = True
        for cil in self.countries:
            if (cil.name == c.name) or \ (cil.xl < c.xl <= cil.xh and \ cil.yl < c.yl <= cil.yh) or \
               (cil.xl < c.xh <= cil.xh and \ cil.yl < c.yh <= cil.yh): append_allowed = False
            break

        if append_allowed:
            if c.xl < self.xl: self.xl = c.xl
            if c.yl < self.yl: self.yl = c.yl
            if c.xh > self.xh: self.xh = c.xh
            if c.yh > self.yh: self.yh = c.yh
            self.countries.append(c)
            return True
        return False

    def generate_world(self):

        country_names = [c.name for c in self.countries]
        self.world = [[city(i, j, country_names) for i in range(self.yl, self.yh)] for j in range(self.xl, self.xh)]
        for country in self.countries:
            for i in range(country.xl, country.xh):
                for j in range(country.yl, country.yh):
                    c = city(i, j, country_names, country.name)
                    self.world[i][j] = c
                    country.add_city(c)
  
    def check_completion(self) -> bool:

        if self.world is None:
            return True
        tc_complete = True
        
        for country in self.countries:
            country_complete = True
            for cc in country.city_coordinates:
                c = self.world[cc.x][cc.y]
                city_complete = True
                for _, val in c.coins.items():
                    if not val:
                        city_complete = False
                        break

                if city_complete:
                    c.complete = 1
                if not c.complete and country_complete:
                    country_complete = False
            if country_complete:
                if not country.complete:
                    country.complete = self.iteration_count
            elif tc_complete:
                tc_complete = False

        if tc_complete:
            self.complete = self.iteration_count
        return tc_complete

    def iteration(self):

        if self.world is not None:
            temp_world = copy.deepcopy(self.world)
            for c in self.countries:
                for cc in c.city_coordinates:
                    self.city_iteration(self.world[cc.x][cc.y], temp_world)
            self.world = temp_world
            self.iteration_count += 1

    def city_iteration(self, c: city, temp_world):

        x_more_then_xl = c.x > self.xl
        x_less_then_xh = c.x < self.xh - 1
        y_more_then_yl = c.y > self.yl
        y_less_then_yh = c.y < self.yh - 1
        for coin, value in c.coins.items():
            diff = value // DEF_COINS_DIV
            if x_more_then_xl and self.world[c.x - 1][c.y].european:
                temp_world[c.x - 1][c.y].coins[coin] += diff
                temp_world[c.x][c.y].coins[coin] -= diff
            if x_less_then_xh and self.world[c.x + 1][c.y].european:
                temp_world[c.x + 1][c.y].coins[coin] += diff
                temp_world[c.x][c.y].coins[coin] -= diff
            if y_more_then_yl and self.world[c.x][c.y - 1].european:
                temp_world[c.x][c.y - 1].coins[coin] += diff
                temp_world[c.x][c.y].coins[coin] -= diff
            if y_less_then_yh and self.world[c.x][c.y + 1].european:
                temp_world[c.x][c.y + 1].coins[coin] += diff
                temp_world[c.x][c.y].coins[coin] -= diff
             
    def show_contries(self):

        print(f"Case number {self.num}")
        sorted_countries = sorted(sorted(self.countries, key = lambda x: x.name), key = lambda x: x.complete)
        for c in sorted_countries:
            c.show()



def iteration(i) -> bool:
    num = int(input())
    if num == 0:
        return False

    tcd = testcase_data(i)
    for _ in range(num):
        input_data = input().split()
        if country.check_input_data(*input_data):
            tcd.add_coutry(country(*input_data))

    tcd.generate_world()
    while not tcd.check_completion():
        tcd.iteration()

    tcd.show_contries()
    return True


if __name__ == "__main__":
    try:
        i = 0
        while iteration(i):
            i += 1
    except Exception as e:
        print(e)
