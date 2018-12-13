using System;
using System.Linq;

namespace day13
{
    class Program
    {
        //private const string file = "test.txt";
        //private const string file = "test2.txt";
        private const string file = "input.txt";

        static void Main(string[] args)
        {
            var board = new Board(file);

            Tuple<int, int> collision = null;
            while (collision == null)
            {
                collision = board.Tick();
            }
            Console.WriteLine(string.Format("Part 1: {0},{1}", collision.Item1, collision.Item2));

            while (board.carts.Count(c => c.Alive) > 1)
                board.Tick();

            var lastAlive = board.carts.First(c => c.Alive);
            Console.WriteLine(string.Format("Part 2: {0},{1}", lastAlive.X, lastAlive.Y));
        }
    }
}
