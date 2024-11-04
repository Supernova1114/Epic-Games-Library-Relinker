
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
    def list_prompt(
        header: str = "Menu:",
        prompt: str = "Select from list",
        option_list: list[str] = []
    ) -> list[int]:

        option_count = len(option_list)

        if option_count == 0:
            print("\nWARNING: Empty options list!")
            return []

        print(f"\n{header}")    

        for index, option in enumerate(option_list):
            print(f"{index + 1}. {option}")    
        
        while True:

                raw_input = input(f"{prompt}\n(\"all\", \"none\", or list \"1,2,3\"): ")

                if raw_input.upper() == "ALL":
                    return list(range(1, option_count + 1))
                elif raw_input.upper() == "NONE":
                    return []
                else:

                    try:
                        selected_options: list[int] = []

                        options_raw: list[str] = raw_input.strip().split(",")
                        
                        for option_str in options_raw:
                            
                            # TODO - continue fixing and test. Should output indexing starting at 1 instead of zero.
                            option_index: int = int(option_str) - 1
                            
                            if option_index >= 0 and option_index < option_count:
                                selected_options.append(option_index)
                        
                        # END for

                        return selected_options

                    except Exception:
                        print("\nWARNING: Invalid input!")
