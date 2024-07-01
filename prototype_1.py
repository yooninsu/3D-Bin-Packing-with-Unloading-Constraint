from py3dbp import Packer, Bin, Item

# Bin 정의 (차량 크기)
bin1 = Bin('vehicle', 100, 100, 100, 100)  # 예시로 가로, 세로, 높이, 무게 용량

# Item 정의 (물품 목록)
items = [
    Item('item1', 10, 20, 15, 5),
    Item('item2', 20, 10, 10, 10),
    Item('item3', 15, 15, 10, 8),
    Item('item4', 30, 10, 20, 20),
    Item('item5', 10, 10, 5, 2)
]

# Packer 초기화
packer = Packer()

# Bin 추가
packer.add_bin(bin1)

# Item 추가
for item in items:
    packer.add_item(item)

# 물품을 Bin에 패킹
packer.pack()

# 결과 출력
for b in packer.bins:
    print("Bin:", b.string())
    print("Packed items:")
    for item in b.items:
        print(" ", item.string())
    print("Unfitted items:")
    for item in b.unfitted_items:
        print(" ", item.string())

# 언로드 비용 최적화 (예시로 단순화)
def optimize_unloading(bins):
    for b in bins:
        # 물품을 언로드 순서에 맞게 정렬 (여기서는 단순히 아이템 이름 순으로)
        b.items.sort(key=lambda x: x.name)
        print("Optimized unloading order for bin:", b.string())
        for item in b.items:
            print(" ", item.string())

# 최적화 실행
optimize_unloading(packer.bins)
