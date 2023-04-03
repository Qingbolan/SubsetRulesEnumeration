import time
from cores.enumerate import enumerate_core
from rule.rule_test import rule_check


def data_query(db, n, k, j, s):
    isFind, results = db.get_by_n_k_j_s(n, k, j, s)

    if not isFind:
        print("No results found in database.")
        return False, [], 0
    else:
        print("reS:", results[0])
        print("reL:", results[1])
        return True, eval(results[0]), results[1]


def example_result(n, k, j, s):
    # 45,8,6,4,4
    reS = [[1, 2, 3, 4, 7, 8], [1, 2, 3, 5, 7, 8], [1, 2, 3, 6, 7, 8], [1, 2, 4, 5, 6, 7], [1, 3, 4, 5, 6, 8],
           [2, 3, 4, 5, 6, 8], [3, 4, 5, 6, 7, 8]]
    reL = 7
    return reS, reL


def core_selection(device,db, m, n, k, j, s):
    localtime = time.asctime(time.localtime(time.time()))
    if m * n * k * j * s != 0:
        # Step1: Query in the current database
        isGet, reS, reL = data_query(db, n, k, j, s)
        print("Step1: Query in the current database.")
        if not isGet:
            print("compute right now.")
            # reS, reL = example_result(n, k, j, s)
            reS, reL = enumerate_core(device,n, k, j, s)
            if not rule_check(reS, n, k, j, s):
                print(">rule check Fail!")
            else:
                print(">rule check pass!")
                # Add record to database
                db.insert(m, n, k, j, s, reS, reL)
                # db.save()
                db.display()
        else:
            print(f"reS:{reS}")
            print(f"reL:{reL}")
        message1 = f"$>{localtime}\n > m={m},n={n},k={k},j={j},s={s}\n > the best length is {reL}\n"
        No = 1
        for _ in reS:
            print(_)
            message1 += str(f" {No}. {_}\n")
            No += 1
    else:
        message1 = f"$>{localtime}\n"
        message1 += "you haven't input completely!\n"
    return message1
