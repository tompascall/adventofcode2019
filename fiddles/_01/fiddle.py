class RocketModule:
    def __init__(self, mass):
        self.mass = mass

    def calc_fuel_by_mass(self, mass):
        return int(mass / 3) - 2

    def fuel(self, mass=None):
        if mass == None:
            mass = self.mass
        fuel_by_mass = self.calc_fuel_by_mass(mass)
        if fuel_by_mass <= 0:
            return 0
        else:
            return fuel_by_mass + self.fuel(fuel_by_mass)


class Rocket:
    def __init__(self, modules):
        self.modules = []
        for module_mass in modules:
            self.add_module(module_mass)

    def add_module(self, module_mass):
        mass = int(module_mass)
        self.modules.append(RocketModule(mass))

    def sum_fuel(self):
        return sum([module.fuel() for module in self.modules])


if __name__ == '__main__':
    with open('./input.txt') as fiddle_input:
        modules = fiddle_input.readlines()
        print(Rocket(modules).sum_fuel())