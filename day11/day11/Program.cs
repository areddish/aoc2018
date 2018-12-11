using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace day11
{
    class Program
    {
        static int RackId(int x, int y)
        {
            return x + 10;
        }

        static int StartingPowerLevel(int x, int y)
        {
            return RackId(x, y) * y;
        }

        static int HundredsDigit(int val)
        {
            return ((int)val / 100) % 10;
        }

        static int PowerLevel(int serial, int x, int y)
        {
            return HundredsDigit((StartingPowerLevel(x, y) + serial) * RackId(x, y)) - 5;
        }

        static Task<Tuple<int, int, int, int>> compute(int[] grid, int n)
        {
            var upperX = 0;
            var upperY = 0;
            var maxPower = 0;
            for (var y = 0; y < 300 - n; y++)
                for (var x = 0; x < 300 - n; x++)
                {
                    var power = 0;
                    for (var j = y; j < y + n; j++)
                        for (var i = x; i < x + n; i++)
                        {
                            power += grid[i + j * 300];
                        }
                    if (power > maxPower)
                    {
                        upperX = x;
                        upperY = y;
                        maxPower = power;
                    }
                }

            // 0-based -> 1-based
            upperX++;
            upperY++;

            return Task.FromResult(new Tuple<int, int, int, int>(upperX, upperY, maxPower, n));
        }

        static void Main(string[] args)
        {
            var serialNumber = 9306;

            var grid = new int[300 * 300];
            for (var y = 0; y < 300; y++)
                for (var x = 0; x < 300; x++)
                {
                    grid[y * 300 + x] = PowerLevel(serialNumber, x + 1, y + 1);
                }

            var part1Solution = Task.Run(() => compute(grid, 3)).Result;
            Console.WriteLine(string.Format("Part 1: {0},{1}", part1Solution.Item1, part1Solution.Item2));

            // Brute force it using all cores.
            List<Task<Tuple<int, int, int, int>>> tasks = new List<Task<Tuple<int, int, int, int>>>();
            for (var n = 1; n < 300; n++)
            {
                // Prevent closure
                var nn = n;
                tasks.Add(Task.Run(() => compute(grid, nn)));
            }

            Task.WhenAll(tasks).Wait();
            var maxPower = tasks.OrderByDescending(t => t.Result.Item3).First().Result;
            Console.WriteLine(string.Format("Part 2: {0},{1},{2}  with power {3}", maxPower.Item1, maxPower.Item2, maxPower.Item4, maxPower.Item3));
        }
    }
}
