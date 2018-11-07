from classes import *

N = 10
DAMNS = ['Боль', 'Жажда', 'Бессоница', 'Дедлайн']
DAY_START = time()

folk = [Person(i) for i in range(1, 31)]
healers = [Healer(damn, DAY_START) for damn in DAMNS]


def main():
    print("Game started at 0")
    print("Everybody sleep")

    rs = RandomState()
    infected_persons = rs.choice(folk, size=N, replace=False)
    damn_names = rs.choice(DAMNS, size=N, replace=True)

    for p, d in zip(infected_persons, damn_names):
        p.damn = d

    sleep(rs.uniform(6, 9))

    print("Everybody woke-up at", time() - DAY_START)
    print("Infected persons:")
    print("\t", end="")
    print("\n\t".join(map(str, infected_persons)))
    print()

    m = Manager(healers)
    m.manage(infected_persons)
    print("All infected persons queued at", time() - DAY_START)

    for healer in healers:
        healer.start()

    # Wait for all threads to complete
    for healer in healers:
        healer.join()

    print("Healers finished their work at", time() - DAY_START)


if __name__ == '__main__':
    main()
