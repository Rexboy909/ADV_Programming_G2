/**
 * Shape interface that defines the contract for all geometric shapes
 */
public interface Shape {
    
    /**
     * Calculate the area of the shape
     * @return the area value
     */
    double calculateArea();
    
    /**
     * Calculate the perimeter of the shape
     * @return the perimeter value
     */
    double calculatePerimeter();
    
    /**
     * Get the name of the shape
     * @return the shape name
     */
    String getShapeName();
}
