"""Module  for breakdown into age groups"""

from sys import argv, stdin
from typing import Dict, List, Union

PersonRow = List[Union[int, str]]  # [age, last, first, middle]


class Society:
    """Class for breakdown into age groups"""

    def __init__(self, ages: List[str]) -> None:
        """Initialize

        Args:
            ages (List[str]): Argv list with ages
        """
        self.ages: List[int] = sorted(list(map(int, ages)))
        self.ages.append(123)  # верхняя «бесконечная» граница
        self.groups: Dict[int, List[PersonRow]] = {i: [] for i in range(len(self.ages))}

    def add_person(self, dump: str) -> None:
        """Function for adding a person to the list

        Args:
            dump (str): String format "<ФИО>, <возраст>"
        """
        line = dump.strip()
        if not line:
            return
        fio_part, age_part = line.split(",", 1)
        fio = fio_part.split()
        while len(fio) < 3:
            fio.append("")
        age = int(age_part.strip())
        person_info: PersonRow = [age, fio[0], fio[1], fio[2]]  # [age, last, first, middle]

        for i, bound in enumerate(self.ages):
            if age <= bound:
                self.groups[i].append(person_info)
                break

    def print(self) -> str:
        """Funtion to print the list of people

        Returns:
            str: data with the current format
        """
        result = ""
        for i in range(len(self.ages) - 1, -1, -1):
            lo = self.ages[i - 1] + 1 if i != 0 else 0
            hi = self.ages[i]
            label = f"{lo}{'+' if hi == 123 else f'-{hi}'}:"
            group = sorted(self.groups[i], key=lambda x: [-int(x[0]), str(x[1]), str(x[2]), str(x[3])])
            group_out = ", ".join(f"{x[1]} {x[2]} {x[3]} ({x[0]})" for x in group)
            line = f"{label} {group_out}"
            print(line)
            result += line + "\n"
        return result


if __name__ == "__main__":
    society = Society(argv[1:])
    for person in stdin.readlines():
        society.add_person(person)
    society.print()
