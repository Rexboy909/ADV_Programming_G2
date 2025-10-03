import java.util.Scanner;

public class FindMedian 
{
    public static void main(String[] args)
    {
        Scanner input = new Scanner(System.in);

        // Ask the user for three integers
        System.out.println("Enter the first integer: ");
        int a = input.nextInt();

        System.out.println("Enter the second integer: ");
        int b = input.nextInt();

        System.out.println("Enter the third integer: ");
        int c = input.nextInt();

        int median;

        // Check if a is the median
        if ((a >= b && a <= c) || (a <= b && a >= c)) {
            median = a;
        }
        // Check if b is the median
        else if ((b >= a && b <= c) || (b <= a && b >= c)) {
            median = b;
        }
        // Otherwise c must be the median
        else {
            median = c;
        }

        // Print out the median
        System.out.println("\nThe median is " + median);

        input.close();
    }
}

