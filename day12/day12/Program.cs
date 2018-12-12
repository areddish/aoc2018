using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace day12
{
    class Program
    {
        static StringBuilder FillWithEmpties(int i)
        {
            StringBuilder sb = new StringBuilder(i);
            for (int j = 0; j < i; j++)
                sb.Append('.');
            return sb;
        }

        static void Main(string[] args)
        {
            // Part1
            Part1();
        }

        #region SOLUTION 1
        static void Part1()
        {
            var data = System.IO.File.ReadAllLines("input.txt");

            int prefix = 6;
            var initialState = "......" + data[0].Split(' ')[2] + ".....";

            List<Tuple<string, char>> rules = new List<Tuple<string, char>>(data.Length - 2);
            foreach (var r in data.Skip(2))
            {
                var parts = r.Split(new string[] { " => " }, StringSplitOptions.RemoveEmptyEntries);
                rules.Add(new Tuple<string, char>(parts[0], parts[1].Trim()[0]));
            }

            int generation = 0;
            while (generation < 20)
            {
                var nextGeneration = FillWithEmpties(initialState.Length);
                foreach (var r in rules)
                {
                    var foundIndex = initialState.IndexOf(r.Item1);
                    while (foundIndex != -1)
                    {
                        nextGeneration[foundIndex + 2] = r.Item2;
                        foundIndex = initialState.IndexOf(r.Item1, foundIndex + 1);
                    }
                }

                nextGeneration.Append(".....");
                var nextGen = nextGeneration.ToString();
                initialState = nextGen;
                // Console.WriteLine(" " + generation + ": " + initialState);

                generation++;
            }

            var sum = 0;
            for (var i = 0; i < initialState.Length; i++)
            {
                sum += (initialState[i] == '#') ? i - prefix : 0;
            }
            Console.WriteLine("Part 1 Sum: " + sum);
        }
        #endregion
    }
}
