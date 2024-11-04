
class MenuCLI:

    @staticmethod
    def yes_no_prompt(prompt: str) -> bool:
        option: str = input(f"{prompt} (y/n): ")
        return len(option) != 0 and str.upper(option[0]) == 'Y'
    
    @staticmethod
    def print_line_separator(char: str = '—', length: int = 40) -> None:
        print(char * length)

    @staticmethod
    def numbered_prompt(
        header: str = "Menu:",
        prompt: str = "Enter an option: ",
        option_list: list[str] = []
    ) -> int:

        option_count = len(option_list)

        if option_count == 0:
            print("\nWARNING: Empty options list!")
            return -1

        while True:

            print(f"\n{header}")        

            for index, option in enumerate(option_list):
                print(f"{index + 1}. {option}")

            try:
                choice = int(input(prompt))

                if choice > 0 and choice <= option_count:
                    print()
                    return choice
                else:
                    print("\nWARNING: Invalid option!")
                
            except ValueError:
                print("\nWARNING: Invalid option!")

    @staticmethod
    def list_prompt():
        ...
