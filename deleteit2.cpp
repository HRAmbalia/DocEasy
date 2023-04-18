#include <iostream> 
using namespace std; 

struct Node 
{ 
    struct Node *left, *right; 
    int key; 
}; 

Node* newNode(int key) 
{ 
    Node *temp = new Node; 
    temp->key = key; 
    temp->left = temp->right = NULL; 
    return temp; 
} 
