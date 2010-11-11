
class Sudoku

    attr_reader :path, :puzzle, :n, :num_guesses

    def initialize path
        @path = path
        @n = 0
        @b = 0
        @puzzle = []
        @num_guesses = 0
        @known_indices = []
        load_puzzle
    end

    def to_s
        s = ''
        current_row = 0
        @puzzle.each_with_index do |c, i|
            r = (i / @n).floor
            s << '\n' if r != current_row
            s << c.to_s
            current_row = r
        end
        return s
    end

    def solve!
        @num_guesses = 0
        r = solve_from! 0, 1
        while r != nil
            r = solve_from! r[0], r[1]
        end
    end

    private

    def solve_from! index, starting_guess
        if index < 0 or index > @puzzle.length
            puts to_s.split '\n'
            raise "Invalid puzzle index #{index} after #{@num_guesses} guesses"
        end

        last_valid_guess_index = nil
        found_valid_guess = false
        (index...@puzzle.length).each do |i|
            unless @known_indices.include? i
                found_valid_guess = false
                (starting_guess..@n).each do |guess|
                    @num_guesses += 1
                    if valid? i, guess
                        found_valid_guess = true
                        last_valid_guess_index = i
                        @puzzle[i] = guess
                        break
                    end
                end
                starting_guess = 1

                if not found_valid_guess
                    break
                end
            end
        end

        if not found_valid_guess
            new_index = index - 1
            new_index = last_valid_guess_index unless last_valid_guess_index == nil
            new_starting_guess = @puzzle[new_index] + 1

            reset_puzzle_at new_index

            while new_starting_guess > @n or @known_indices.include? new_index
                new_index -= 1
                new_starting_guess = @puzzle[new_index] + 1
                reset_puzzle_at new_index
            end

            return [new_index, new_starting_guess]
        else
            return nil
        end
    end

    def reset_puzzle_at index
        (index...@puzzle.length).each do |i|
            unless @known_indices.include? i
                @puzzle[i] = 0
            end
        end
    end

    def valid? index, guess
        # check column
        col_index = index % @n
        (0...@n).each do |r|
            r_index = col_index + (@n * r)
            unless r_index == index
                if @puzzle[r_index] == guess
                    return false
                end
            end
        end

        # check row
        row_index = (index / @n).floor
        start = @n * row_index
        finish = start + @n
        (start...finish).each do |c_index|
            unless c_index == index
                if @puzzle[c_index] == guess
                    return false
                end
            end
        end

        # check block
        return valid_for_block? index, guess
    end

    def valid_for_block? index, guess
        row_index = (index / @n).floor
        col_index = index % @n

        block_row = (row_index / @b).floor
        block_col = (col_index / @b).floor

        row_start = block_row * @b
        row_end = row_start + @b - 1
        col_start = block_col * @b
        col_end = col_start + @b - 1

        (row_start..row_end).each do |r|
            (col_start..col_end).each do |c|
                i = c + (r * @n)
                if @puzzle[i] == guess
                    return false
                end
            end
        end

        return true
    end

    def load_puzzle
        @n = 0
        @puzzle = []
        File::open(@path, 'r') do |file|
            i = 0
            while content = file.gets
                @n = content.to_s.length - 1 if @n == 0
                content.to_s.each_char do |c|
                    if c =~ /\d/
                        @puzzle << c.to_i
                        @known_indices << i if c.to_i != 0
                        i += 1
                    end
                end
            end
        end
        @b = Math.sqrt(@n).to_i
    end

end


if __FILE__ == $0
    s = Sudoku.new ARGV[0]

    puts
    puts 'Puzzle:'
    puts s.to_s.split '\n'
    puts

    puts 'Solution:'
    s.solve!
    puts s.to_s.split '\n'
    puts "Number of guesses: #{s.num_guesses}"
    puts
end
