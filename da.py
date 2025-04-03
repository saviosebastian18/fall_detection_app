n=int(input())
arr = list(map(int, input().split()))
odd=0
even=0
for b in arr:
    if b%2==0:
        even+=1
    else:
        odd+=1
print(even)
print(odd)



n=int(input())
arr = list(map(int, input().split()))
for i in range(len(arr)-1, -1,-1):
    print(arr[i],end=" ")

    n=int(input())
arr = list(map(int, input().split()))
s=0
for b in arr:
    s=s+b
    
print(s)    
    

    n=int(input())
arr = list(map(int, input().split()))
for i in arr:
    if arr.count(i) >= (n/2):
        print(f"The majority element is : {i}")
        break
else:
    print("No majority element found in the array")
    
    
    