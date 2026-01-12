/**
 * ShapeApp - Entry point for the Shape hierarchy application
 */
public class ShapeApp {
    
    public static void main(String[] args) {
        // Create instances of different shapes
        Shape circle = new Circle(5);
        Shape rectangle = new Rectangle(4, 6);
        Shape triangle = new Triangle(3, 4, 5);
        
        // Create an array of shapes
        Shape[] shapes = {circle, rectangle, triangle};
        
        // Display information about each shape
        System.out.println("=== Shape Hierarchy Demonstration ===\n");
        
        for (Shape shape : shapes) {
            System.out.println("Shape: " + shape.getShapeName());
            System.out.printf("Area: %.2f%n", shape.calculateArea());
            System.out.printf("Perimeter: %.2f%n", shape.calculatePerimeter());
            System.out.println();
        }
        
        // Calculate total area
        double totalArea = 0;
        for (Shape shape : shapes) {
            totalArea += shape.calculateArea();
        }
        System.out.printf("Total area of all shapes: %.2f%n", totalArea);
    }
}
