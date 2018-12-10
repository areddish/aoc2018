using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;

namespace day10
{
    class Program
    {
        private const string file = @"c:\src\aoc2018\day10\test.txt";
        //private const string file = @"c:\src\aoc2018\day10\input.txt";

        private const string bmpFileName = "solution.bmp";

        static void Render(List<int> xs, List<int> ys)
        {
            var offsetx = Math.Abs(xs.Min());
            var offsety = Math.Abs(ys.Min());

            var mx = xs.Max() + offsetx + 1;
            var my = ys.Max() + offsety + 1;

            Bitmap bp = new Bitmap(mx, my);

            // Fill in the background with XNA throwback color :)
            for (var y = 0; y < my; y++)
                for (var x = 0; x < mx; x++)
                    bp.SetPixel(x, y, Color.CornflowerBlue);

            // Draw the message
            for (var i = 0; i < xs.Count; i++)
            {
                bp.SetPixel(xs[i] + offsetx, ys[i] + offsety, Color.Yellow);
            }

            bp.Save(bmpFileName);
        }

        static void Main(string[] args)
        {
            var data = System.IO.File.ReadAllLines(file);

            // Parallel arrays
            var xs = new List<int>();
            var ys = new List<int>();
            var dxs = new List<int>();
            var dys = new List<int>();

            foreach (var d in data)
            {
                // position=< 1,  8> velocity=< 1, -1>
                var parts = d
                    .Split(new string[] { "position=<", ", ", "> velocity=<", ">" }, StringSplitOptions.RemoveEmptyEntries);

                var x = int.Parse(parts[0]);
                var y = int.Parse(parts[1]);
                var dx = int.Parse(parts[2]);
                var dy = int.Parse(parts[3]);
                xs.Add(x - 1);
                ys.Add(y - 1);
                dxs.Add(dx);
                dys.Add(dy);
            }

            var prevXBboxWidth = xs.Max() + Math.Abs(xs.Min());
            var prevYBboxWidth = ys.Max() + Math.Abs(ys.Min());
            var prevXDelta = -1;
            var prevYDelta = -1;

            var seconds = 0;
            while (true)
            {
                // Update the positions from velocity
                for (var i = 0; i < xs.Count; i++)
                {
                    xs[i] += dxs[i];
                    ys[i] += dys[i];
                }

                // Track how many sections it takes
                seconds++;

                // Check for convergences. When they maxes start to get big again, stop!
                var currentXBboxWidth = xs.Max() + Math.Abs(xs.Min());
                var currentYBboxWidth = ys.Max() + Math.Abs(ys.Min());

                var bboxXDelta = (currentXBboxWidth - prevXBboxWidth);
                var bboxYDelta = (currentYBboxWidth - prevYBboxWidth);

                // We've converged when there is no longer a change in the bounding box. But the pixels may still settle.
                if (bboxXDelta > 0 || bboxYDelta > 0 || (prevXDelta == 0 && bboxXDelta != 0) || (prevYDelta == 0 && bboxYDelta != 0))
                {
                    // The points are scattering again, the previous step was the solution. Roll back.
                    for (var i = 0; i < xs.Count; i++)
                    {
                        xs[i] -= dxs[i];
                        ys[i] -= dys[i];
                    }

                    // Write the possible solution
                    Render(xs, ys);
                    break;
                }

                prevXBboxWidth = currentXBboxWidth;
                prevYBboxWidth = currentYBboxWidth;

                prevXDelta = bboxXDelta;
                prevYDelta = bboxYDelta;
            }

            Console.WriteLine("Part 1 solution in bmp file: solution.bmp");
            Console.WriteLine(string.Format("Part 2 took {0} seconds.", seconds - 1));
        }
    }
}
