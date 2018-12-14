using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Text;

namespace day14
{
    class Program
    {
        static void Main(string[] args)
        {
            Stopwatch sw = new Stopwatch();
            sw.Start();
            Part1();
            sw.Stop();
            Console.WriteLine("Part 1: timing: " + sw.ElapsedMilliseconds + "ms");
            sw.Restart();
            Part2();
            sw.Stop();
            Console.WriteLine("Part 2: timing: " + sw.ElapsedMilliseconds + "ms");
        }

        static void Part1()
        {
            List<int> recipes = new List<int>();
            recipes.Add(3);
            recipes.Add(7);

            int elf1Index = 0;
            int elf2Index = 1;

            int desired = 84601;
            while (recipes.Count < desired + 10)
            {
                int score1 = recipes[elf1Index];
                int score2 = recipes[elf2Index];

                int sum = score1 + score2;
                if (sum >= 10)
                {
                    recipes.Add(((int)(sum / 10) % 10));
                }
                recipes.Add(sum % 10);

                elf1Index += score1 + 1;
                elf1Index %= recipes.Count;

                elf2Index += score2 + 1;
                elf2Index %= recipes.Count;
            }

            Console.Write("Part 1: ");
            for (var i = desired; i < desired + 10; i++)
                Console.Write(recipes[i]);
            Console.WriteLine();
        }

#if MATCH_REVERSED_NUMERICAL
        static bool Match(LinkedList<int> last, int val)
        {
            var n = 0;
            var n2 = 0;
            var skipFirst = false;
            int ni = 0;
            int ni2 = 0;
            foreach (var d in last)
            {
                n += d * (int)Math.Pow(10, ni);
                ni++;
                if (skipFirst)
                {
                    n2 += d * (int)Math.Pow(10, ni2);
                    ni2++;
                }
                skipFirst = true;
            }

            n %= (int)Math.Pow(10, ni -1);

           // Console.WriteLine($"{n} {n2} {val}");
            return n == val || n2 == val;
        }
#endif

        static bool MatchStr(LinkedList<int> last, string val)
        {
            StringBuilder sb = new StringBuilder(last.Count);

            foreach (var d in last)
            {
                sb.Append(d.ToString());
            }
            return sb.ToString().IndexOf(val) != -1;
        }

        static void Part2()
        {
            // My input starts with a zero, so compute it in reverse.
            var input = "084601";
            List<int> recipes = new List<int>();
            recipes.Add(3);
            recipes.Add(7);

            int elf1Index = 0;
            int elf2Index = 1;

            int recipeCount = 2;
            int inputCount = input.Length;

            LinkedList<int> lastN = new LinkedList<int>();
            while (true)
            {
                int score1 = recipes[elf1Index];
                int score2 = recipes[elf2Index];

                int sum = score1 + score2;
                if (sum >= 10)
                {
                    int digit = ((int)(sum / 10) % 10);
                    recipes.Add(digit);
                    lastN.AddLast(digit);
                    recipeCount++;
                }
                recipes.Add(sum % 10);
                lastN.AddLast(sum % 10);

                elf1Index = (elf1Index + score1 + 1) % recipes.Count;
                elf2Index = (elf2Index + score2 + 1) % recipes.Count;

                recipeCount++;

                // It's possible to get a two digit number at the end so we'll handle that by doing two comparisons.
                // One of the first inputCount and one of the last inputCount. i.e.
                //  1235510 can match 123551 or 235510.
                while (lastN.Count > inputCount + 1)
                    lastN.RemoveFirst();

                // Technically we could further scope this and make it run faster by checking if sum == the ending. There's an
                // edge case though where we end in 1 or 0 and then we have to watch out for sum == 10 or 0 or 1.
                if (lastN.Count >= inputCount)
                {
                    // This compares via string, the intial solution compares using integers but that will have issues with leading 0's.
                    // A solution that works is to compare a reversed number if it's a leading 0. That's the faster solution and shaves
                    // a few seconds off the execution. But this is more straightforward for now.
                    if (MatchStr(lastN, input))
                    {
                        // Solution is the current recipe count - the count of recipes we are looking for.
                        // If the last sum was a two digit number we need to disregard it
                        Console.WriteLine("Part 2:" + (recipes.Count - inputCount - ((sum >= 10) ? 1 : 0)));
                        return;
                    }
                }
            }
        }
    }
}
