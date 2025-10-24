public class search {
    public static void main(String[] args) {
        int[] numbers = new int[100]; // CHANGE DATA SIZE HERE
        for (int i = 0; i < numbers.length; i++) {
            numbers[i] = 3 + 2 * i; // fills with 3,5,7,... (100 numbers)
        }
        
        int target = 47; // CHANGE TARGET HERE. ODD NUMBERS ONLY FOR THIS DATA SET

        int start = 0;
        int end = numbers.length - 1;
        int attempts = 1;
        System.out.println("Target is : " + target);
        System.out.println();
        binarySearch(numbers, target, start, end, attempts);
    }

    public static int binarySearch(int[] arr, int target, int start, int end, int amt) {
        int mid = start + (end - start) / 2; // Finding the bounds of the array and setting a mid point
        if (arr[mid] == target){
            System.out.println("Target found at index: ");
            System.out.println(mid);
             System.out.println("It took " + (amt)+" passes to find the target.");
            return 1;
        }

        if (arr[mid] > target) {
            System.out.println("Searching left half of the array");
            System.out.println("Current mid index: " + mid);
            System.out.println("Current number at array: " + arr[mid]);
            System.out.println("Currently at pass " + (amt));
            System.out.println();
            System.out.println();
            amt ++;
            return binarySearch(arr, target, start, mid-1, amt);
        }

        if (arr[mid] < target) {
            System.out.println("Searching right half of the array");
            System.out.println("Current mid index: " + mid);
            System.out.println("Current number at array: " + arr[mid]);
            System.out.println("Currently at pass " + (amt));
            System.out.println();
            System.out.println();
            amt ++;
            return binarySearch(arr, target, mid+1, end, amt);
        }
        System.out.println("Target not found");
        return -1; // Target not found
    }
}