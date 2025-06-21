#### Pointer in C
A pointer in C is a variable that stores the memory address of another variable. Pointers are used to dynamically allocate memory, store addresses, and access variables indirectly.

Example 1: Basic Pointer Usage

```c
#include <stdio.h>

int main() {
    int num = 10;      // Regular integer variable
    int *ptr = &num;   // Pointer that stores the address of num
    
    printf("Value of num: %d\n", num);           // Prints 10
    printf("Address of num: %p\n", (void*)&num); // Prints memory address of num
    printf("Value pointed to by ptr: %d\n", *ptr); // Dereferencing the pointer, prints 10
    
    return 0;
}
```
Example 2: Pointer to Pointer
```c

#include <stdio.h>

int main() {
    int num = 5;
    int *ptr = &num;        // Pointer to an integer
    int **ptr2 = &ptr;      // Pointer to a pointer

    printf("Value of num: %d\n", num);             // 5
    printf("Value via ptr: %d\n", *ptr);           // 5
    printf("Value via ptr2: %d\n", **ptr2);        // 5
    
    return 0;
}
```

#### 2. Algorithm (Time Complexity)
Time complexity is a way to express the efficiency of an algorithm by measuring the amount of time it takes relative to the input size. The complexity is often expressed using Big-O notation, such as O(1), O(n), O(log n), etc.

```c
Example 1: O(1) - Constant Time Complexity
c
Copy code
#include <stdio.h>

void printFirstElement(int arr[], int size) {
    printf("First element: %d\n", arr[0]);  // Constant time, always the same operation
}

int main() {
    int arr[] = {1, 2, 3, 4, 5};
    printFirstElement(arr, 5);  // O(1)
    
    return 0;
}
```


Example 2: O(n) - Linear Time Complexity

```c
#include <stdio.h>

void printElements(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);  // Linear time, iterates over all elements
    }
    printf("\n");
}

int main() {
    int arr[] = {1, 2, 3, 4, 5};
    printElements(arr, 5);  // O(n)
    
    return 0;
}
```

Example 3: O(n^2) - Quadratic Time Complexity

```c
#include <stdio.h>

void printPairs(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            printf("(%d, %d) ", arr[i], arr[j]);  // Quadratic time, nested loops
        }
    }
    printf("\n");
}

int main() {
    int arr[] = {1, 2, 3};
    printPairs(arr, 3);  // O(n^2)
    
    return 0;
}

```
#### Stack in C
A stack is a linear data structure that follows the Last-In-First-Out (LIFO) principle. Elements are added (pushed) and removed (popped) from the top of the stack.

Example 1: Stack Using Arrays

```c
#include <stdio.h>
#include <stdlib.h>

#define MAX 5  // Maximum size of the stack

// Stack structure
struct Stack {
    int arr[MAX];
    int top;
};

// Initialize stack
void initStack(struct Stack* stack) {
    stack->top = -1;
}

// Push element onto stack
void push(struct Stack* stack, int value) {
    if (stack->top == MAX - 1) {
        printf("Stack Overflow\n");
    } else {
        stack->arr[++(stack->top)] = value;
        printf("%d pushed to stack\n", value);
    }
}

// Pop element from stack
int pop(struct Stack* stack) {
    if (stack->top == -1) {
        printf("Stack Underflow\n");
        return -1;
    } else {
        return stack->arr[(stack->top)--];
    }
}

// Display the stack
void display(struct Stack* stack) {
    if (stack->top == -1) {
        printf("Stack is empty\n");
    } else {
        printf("Stack elements: ");
        for (int i = stack->top; i >= 0; i--) {
            printf("%d ", stack->arr[i]);
        }
        printf("\n");
    }
}

int main() {
    struct Stack stack;
    initStack(&stack);
    
    push(&stack, 10);  // 10 pushed
    push(&stack, 20);  // 20 pushed
    push(&stack, 30);  // 30 pushed
    
    display(&stack);   // Display stack
    
    printf("%d popped from stack\n", pop(&stack)); // 30 popped
    
    display(&stack);   // Display stack after pop
    
    return 0;
}
```
Example 2: Stack Using Linked List

```c
#include <stdio.h>
#include <stdlib.h>

// Stack node structure
struct StackNode {
    int data;
    struct StackNode* next;
};

// Function to push an element to the stack
void push(struct StackNode** root, int data) {
    struct StackNode* newNode = (struct StackNode*) malloc(sizeof(struct StackNode));
    if (!newNode) {
        printf("Memory allocation failed\n");
        return;
    }
    newNode->data = data;
    newNode->next = *root;
    *root = newNode;
    printf("%d pushed to stack\n", data);
}

// Function to pop an element from the stack
int pop(struct StackNode** root) {
    if (*root == NULL) {
        printf("Stack is empty\n");
        return -1;
    }
    struct StackNode* temp = *root;
    int popped = temp->data;
    *root = (*root)->next;
    free(temp);
    return popped;
}

// Function to display the stack
void display(struct StackNode* root) {
    if (root == NULL) {
        printf("Stack is empty\n");
    } else {
        printf("Stack elements: ");
        while (root != NULL) {
            printf("%d ", root->data);
            root = root->next;
        }
        printf("\n");
    }
}

int main() {
    struct StackNode* stack = NULL;

    push(&stack, 10);  // 10 pushed
    push(&stack, 20);  // 20 pushed
    push(&stack, 30);  // 30 pushed

    display(stack);    // Display stack
    
    printf("%d popped from stack\n", pop(&stack)); // 30 popped
    
    display(stack);    // Display stack after pop
    
    return 0;
}

```
