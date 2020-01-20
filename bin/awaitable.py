import asyncio
x = [{'skip': False, 'group': False, 'name': 'capitolcomplex', 'proj': ['null'], 'planarray': ['143', '124', '127'], 'hassite': 'amp'}, {'skip': False, 'group': False, 'name': 'audicentralhouston', 'proj': ['null'], 'planarray': ['126', '125', '124'], 'hassite': 'amp'}, {'skip': False, 'group': False, 'name': '425riverside', 'proj': ['3'], 'planarray': ['0', '2', '3', '4'], 'hassite': ['qv']}, {'skip': False, 'group': True, 'name': 'harbourbridge', 'proj': ['14'], 'planarray': ['0'], 'hassite': 'qv'}, {'skip': True, 'group': True, 'name': 'unioncityintermodal', 'proj': ['null'], 'planarray': ['4', '5', '6'], 'hassite': 'amp'}, {'skip': True, 'group': True, 'name': 'redbeach', 'proj': ['null'], 'planarray': ['124', '125'], 'hassite': 'amp'}, {'skip': True, 'group': True, 'name': 'santabarbaratjwall', 'proj': ['null'], 'planarray': ['124'], 'hassite': 'amp'}, {'skip': True, 'group': True, 'name': 'beverlyhillshigh', 'proj': ['null'], 'planarray': ['124'], 'hassite': 'amp'}, {'skip': True, 'group': True, 'name': 'isabelladam', 'proj': ['null'], 'planarray': ['1'], 'hassite': 'amp'}, {'skip': True, 'group': True, 'name': '755fig', 'proj': ['null'], 'planarray': ['2', '3'], 'hassite': 'amp'}, {'skip': True, 'group': True, 'name': 'haieng', 'proj': ['null'], 'planarray': ['6', '7'], 'hassite': 'amp'}, {'skip': True, 'group': True, 'name': 'tesolongbeach8485', 'proj': ['null'], 'planarray': ['124', '125', '127'], 'hassite': 'amp'}, {'skip': True, 'group': True, 'name': 'natoma', 'proj': ['2'], 'planarray': ['0', '3'], 'hassite': 'qv'}, {'skip': True, 'group': True, 'name': 'TarzanaMed', 'proj': ['22'], 'planarray': ['0', '1', '2', '3'], 'hassite': 'qv'}, {'skip': True, 'group': True, 'name': 'LasVegasproj', 'proj': ['14'], 'planarray': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15'], 'hassite': 'qv'}, {'skip': True, 'group': True, 'name': 'texasinternational', 'proj': ['24'], 'planarray': ['2'], 'hassite': 'qv'}]
async def factorial(skip, group, name, *args):
    f = 1
    for i in range(2, number + 1):
        print(f"Task {name}: Compute factorial({i})...")
        await asyncio.sleep(1)
        f *= i
    print(f"Task {name}: factorial({number}) = {f}")

async def main():
    # Schedule three calls *concurrently*:
    await asyncio.gather(
        for each in projects:
            factorial(each)
    )
    asyncio.gather(
        *[coro(
            "group 1.{}".format(i)
            ) for i in range(1, 6)
          ]
        )
asyncio.run(main())

# Expected output:
#
#     Task A: Compute factorial(2)...
#     Task B: Compute factorial(2)...
#     Task C: Compute factorial(2)...
#     Task A: factorial(2) = 2
#     Task B: Compute factorial(3)...
#     Task C: Compute factorial(3)...
#     Task B: factorial(3) = 6
#     Task C: Compute factorial(4)...
#     Task C: factorial(4) = 24