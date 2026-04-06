import torch

tester = torch.tensor([[1,5,6,7,8,9,6,5],[5,6,0,7,8,9,6,5],[7,0,1,6,8,9,6,5],[9,1,2,9,4,7,6,5],[1,5,6,7,8,9,6,5],[3,9,6,5,1,5,6,7],[1,5,6,7,8,9,6,5],[1,5,6,7,8,9,6,5]])

test2 = torch.tensor([[0,2,6,3,9,7,4,5],[1,1,0,2,1,6,5,4],[6,6,5,4,2,1,9,8],[4,1,2,9,2,7,6,5],[3,5,1,6,8,4,5,9],[3,5,7,8,9,5,4,1],[3,6,5,4,1,9,7,5],[1,2,5,6,4,7,8,9]])

input = abs(tester - test2)

    dist_mat = torch.zeros(len(input) - 1, len(input) - 1)
    dist_sub = torch.zeros(len(input) - 1, len(input) - 1)
    
    
    for k in range(len(dist_mat)):
        dist_mat[k,:-k] = input[:-(k+1)]  
        dist_sub[k,:-k] = input[(k+1):]
        
        # Add the mirror.
        dist_mat[k:,-(k + 1)] = torch.fliplr(input[:-(k+1)])
        dist_sub[k:,-(k + 1)] = torch.fliplr(input[:-(k+1)]) 
    
    dist_mat = abs(dist_mat - dist_sub)
    
    dist_out = torch.zeros(input.size())

    mask_new = torch.zeros((8,8))
    
    for k, row in enumerate(dist_mat):
        mask_new[k:] = row[:-k]
        mask_new[:k] = torch.fliplr(row[-k:])
        
    mask_up = torch.zeros((9,9))
    mask_down = torch.zeros((9,9))
    
    mask_up[:-1, :-1] = torch.triu(mask_new)
    mask_down[1:, 1:] = torch.tril(mask_new)

    dist_out = mask_up + mask_down
    
mask_up = torch.zeros((9,9))
mask_down = torch.zeros((9,9))
mask_up[:-1, :-1] = torch.fliplr(torch.triu(tester))
mask_down[1:, 1:] = torch.fliplr(torch.tril(tester))

print(mask_up)
print(mask_down)
print(mask_up + mask_down)
### Have to assume all distances = 1
dist_out = torch.zeros(input.size())
mask_up = torch.triu(dist_mat) > 0 
mask_down = torch.tril(dist_mat) > 0
mask = torch.zeros(input.size())
mask[:-1, :-1] = dist_mat[mask_up]
dist_out[1:, 1:] = dist_mat[mask_down]

print(mask)

dist_out = torch.fliplr(dist_out)

print(mask)

dist_out[mask] = dist_mat

print(empty)