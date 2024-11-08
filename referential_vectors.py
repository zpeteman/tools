import numpy as np

class CoordinateConverter:
    def __init__(self, x=None, y=None, z=None, r=None, theta=None, phi=None, rho=None):
        # Initialize coordinates; you can specify them in any form.
        self.x = x
        self.y = y
        self.z = z
        self.r = r
        self.theta = theta
        self.phi = phi
        self.rho = rho

    def car2cyle(self):
        """Convert from Cartesian to Cylindrical coordinates."""
        self.rho = np.sqrt(self.x**2 + self.y**2)
        self.phi = np.arctan2(self.y, self.x)
        # self.z remains the same
        return (self.rho, self.phi, self.z)

    def cyle2Sph(self):
        """Convert from Cylindrical to Spherical coordinates."""
        if self.rho is None or self.z is None:
            raise ValueError("rho and z must be defined to convert from Cylindrical to Spherical coordinates.")
        self.r = np.sqrt(self.rho**2 + self.z**2)
        self.theta = np.arctan2(self.rho, self.z)
        return (self.r, self.theta, self.phi)

    def sph2car(self):
        """Convert from Spherical to Cartesian coordinates."""
        if self.r is None or self.theta is None or self.phi is None:
            raise ValueError("r, theta, and phi must be defined to convert from Spherical to Cartesian coordinates.")
        self.x = self.r * np.sin(self.theta) * np.cos(self.phi)
        self.y = self.r * np.sin(self.theta) * np.sin(self.phi)
        self.z = self.r * np.cos(self.theta)
        return (self.x, self.y, self.z)

    def set_cartesian(self, x, y, z):
        """Set Cartesian coordinates and reset other coordinates."""
        self.x, self.y, self.z = x, y, z
        self.rho = self.phi = self.r = self.theta = None  # Clear other coordinates

    def set_cylindrical(self, rho, phi, z):
        """Set Cylindrical coordinates and reset other coordinates."""
        self.rho, self.phi, self.z = rho, phi, z
        self.x = self.y = self.r = self.theta = None  # Clear other coordinates

    def set_spherical(self, r, theta, phi):
        """Set Spherical coordinates and reset other coordinates."""
        self.r, self.theta, self.phi = r, theta, phi
        self.x = self.y = self.z = self.rho = None  # Clear other coordinates

    def convert(self, from_system, to_system):
        """
        Convert between coordinate systems. Supported systems:
        - 'cartesian'
        - 'cylindrical'
        - 'spherical'
        """
        if from_system == 'cartesian' and to_system == 'cylindrical':
            return self.car2cyle()
        elif from_system == 'cylindrical' and to_system == 'spherical':
            return self.cyle2Sph()
        elif from_system == 'spherical' and to_system == 'cartesian':
            return self.sph2car()
        else:
            raise ValueError(f"Conversion from {from_system} to {to_system} is not supported.")



import numpy as np

class Vects:
    def __init__(self, x1=None, y1=None, z1=None, x2=None, y2=None, z2=None, md1=None, md2=None, ang=None):
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1
        self.md1 = md1
        self.x2 = x2
        self.y2 = y2
        self.z2 = z2
        self.md2 = md2
        self.ang = ang

    def CC(self):
        """Calculate the Cartesian coordinate dot product."""
        self.CP = self.x1 * self.x2 + self.y1 * self.y2 + self.z1 * self.z2
        return self.CP

    def CT(self):
        """Calculate the trigonometric dot product."""
        self.CP = self.md1 * self.md2 * np.cos(self.ang)
        return self.CP

    def MDC(self):
        """Calculate the Cartesian coordinate cross product magnitude."""
        self.DP = np.sqrt(
            (self.y1 * self.z2 - self.z1 * self.y2) ** 2 + 
            (self.x1 * self.z2 - self.z1 * self.x2) ** 2 + 
            (self.x1 * self.y2 - self.y1 * self.x2) ** 2
        )
        return self.DP

    def MDT(self):
        """Calculate the trigonometric cross product magnitude."""
        self.DP = self.md1 * self.md2 * np.sin(self.ang)
        return self.DP

    def convert(self, Trig):
        """Choose the appropriate methods based on Trig flag."""
        if Trig == False:
            # Call CC and MDC methods and return their results
            return (self.CC(), self.MDC())
        elif Trig == True:
            # Call CT and MDT methods and return their results
            return (self.CT(), self.MDT())

print('welcome to the wizardly app of point material mechanics \n ')
print(" - changing the referential (press 1). \n - vector calculation (press 2).")
opp = input("press the corresponding num for what u need basterd : ")

if opp == "1" :
    print("soo u wants to change the referential bastard hahaha.")
    print("your vector is expressed in which system ??  (inswer by 'Cartezian', 'Cylendric' or 'Spheric')")
    coo = input('in which system is yours ?? ')
    if coo == "Cartezian" :
        x = float(input('the x value :'))
        y = float(input('the y value : '))
        z = float(input('the z value : '))

        '''cartezian to cylendric'''
        print("let's start by the Cylendrical coordonites : ")
        converter = CoordinateConverter(x=x, y=y, z=z)
        rho, phi ,z = converter.convert('caretsian', 'cylindrical')
        print("Cylindrical:", converter.convert('cartesian', 'cylindrical'))

        
        #cartizian to spheric
        print("here the sphericals now : ")
        converter = CoordinateConverter(rho=rho, phi=phi, z=z)
        print("Spherical:", converter.convert('cylindrical','spherical'))



    elif coo == "Cylendric" :
        rho = float(input('the rho value :'))
        phi = float(input('the phi value : '))
        z = float(input('the z value : '))

        #cylendric to spheric
        pritn("the spherical values are :")
        converter = CoordinateConverter(rho=rho,phi=phi, z =z)
        r, theta, phi = converter.convert('cylindrical', 'spherical')
        print('spherical:',converter.convert('cylindrical','spherical'))

        #cylendric to cartezian
        print("now the cartizian :")
        converter = CoordinateConverter(r=r, theta=theta, phi=phi)
        print('Cartesian :', converter.convert('spherical','cartesian'))

    elif coo == "Spheric" :
        r = float(input('the r value : '))
        theta = float(input('the theta value : '))
        phi = float(input('the phi value : '))

        #spheric to cartezian
        print("the cartizian values are :")
        converter = CoordinateConverter(r=r, theta=theta, phi=phi)
        x, y , z = converter.convert('spherical','cartesian')
        print('Cartesian :', converter.convert('spherical','cartesian'))

        #spherical to cyclic 
        print("the Cylendricals are : ")
        converter = CoordinateConverter(x=x, y=y, z=z)
        print("Cylindrical:", converter.convert('cartesian', 'cylindrical'))     


elif opp == "2":
    choice = input('do u have the angel between the two vectors ?? (y/n)')
    if choice == 'y':
        md1 = float(input('enter the module of the first vector : '))
        md2 = float(input('enter the module of the second vector : '))
        ang = float(input('enter the angel between the vectors :'))

        vector = Vects(md1=md1,md2=md2, ang=ang)
        dot,cross = vector.convert(Trig=True)
        print(f'the value of the cross product is {cross}, and the module of the dot product is {dot}')
        
    elif choice == 'n':
        x1 = float(input('enter the x value for the first vector : '))
        y1 = float(input('enter the y value for the first vector : '))
        z1 = float(input('enter the z value for the first vector : '))

        x2 = float(input('enter the x value for the second vector : '))
        y2 = float(input('enter the y value for the second vector : '))
        z2 = float(input('enter the z value for the second vector : '))

        vector = Vects(x1=x1, y1=y1, z1=z1, x2=x2, y2=y2,z2=z2)
        dot,cross = vector.convert(Trig=False)
        print(f'the value of the cross product is {cross}, and the module of the dot product is {dot}')
