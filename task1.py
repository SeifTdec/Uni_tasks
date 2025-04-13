import math

class Rectangle:
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width

    def perimeter(self):
        return 2 * (self.length + self.width)

class Circle:
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

    def circumference(self):
        return 2 * math.pi * self.radius

rectangle1 = Rectangle(5, 10)
rectangle2 = Rectangle(7, 3)

circle1 = Circle(4)
circle2 = Circle(6)

rect1_area = rectangle1.area()
rect1_perimeter = rectangle1.perimeter()
rect2_area = rectangle2.area()
rect2_perimeter = rectangle2.perimeter()

circ1_area = circle1.area()
circ1_circumference = circle1.circumference()
circ2_area = circle2.area()
circ2_circumference = circle2.circumference()
print(f"Rectangle 1 Area: {rect1_area}, Perimeter: {rect1_perimeter}")
print(f"Rectangle 2 Area: {rect2_area}, Perimeter: {rect2_perimeter}")
print(f"Circle 1 Area: {circ1_area}, Circumference: {circ1_circumference}")
print(f"Circle 2 Area: {circ2_area}, Circumference: {circ2_circumference}")

if rect1_area > rect2_area:
    print("Rectangle 1 has a larger area than Rectangle 2")
elif rect1_area < rect2_area:
    print("Rectangle 2 has a larger area than Rectangle 1")
else:
    print("Both rectangles have the same area")

if circ1_area > circ2_area:
    print("Circle 1 has a larger area than Circle 2")
elif circ1_area < circ2_area:
    print("Circle 2 has a larger area than Circle 1")
else:
    print("Both circles have the same area")
