using System;
using System.Collections.Generic;
using System.Linq;

namespace day13
{
    public class Board
    {
        // Convert from char -> Direction
        static Dictionary<char, Direction> cartToDirectionMap = new Dictionary<char, Direction>()
                {
                    { '>' , Direction.Right },
                    { '<' , Direction.Left},
                    { 'v' , Direction.Down },
                    { '^' , Direction.Up }
                };

        // Offsets per Direction
        static Dictionary<Direction, Tuple<int, int>> directionToOffsetMap = new Dictionary<Direction, Tuple<int, int>>
                {
                    { Direction.Right,  new Tuple<int, int>(1, 0) },
                    { Direction.Left, new Tuple<int, int>(-1, 0) },
                    { Direction.Down, new Tuple<int, int>(0, 1) },
                    { Direction.Up, new Tuple<int, int>(0, -1) }
                };

        // Transition per direction, per path item
        static Dictionary<Direction, Dictionary<char, Direction>> transitionMap = new Dictionary<Direction, Dictionary<char, Direction>>()
            {
                { Direction.Right, new Dictionary<char, Direction>()
                    {
                        { '\\', Direction.Down },
                        { '/', Direction.Up },
                        { '-', Direction.Right }
                    }},
                { Direction.Left, new Dictionary<char, Direction>()
                    {
                        { '\\', Direction.Up },
                        { '/', Direction.Down },
                        { '-', Direction.Left }
                    }},
                { Direction.Down, new Dictionary<char, Direction>()
                    {
                        { '\\', Direction.Right },
                        { '/', Direction.Left },
                        { '|', Direction.Down }
                    }},
                { Direction.Up, new Dictionary<char, Direction>()
                    {
                        { '\\', Direction.Left },
                        { '/', Direction.Right },
                        { '|', Direction.Up }
                    }}
            };

        private char[] board;
        private int width;
        private int height;
        public List<Cart> carts;

        public Board(string filename)
        {
            var data = System.IO.File.ReadAllLines(filename);

            this.width = data[0].Length;
            this.height = data.Length;

            this.board = new char[width * height];
            this.carts = new List<Cart>();

            this.ParseBoard(data);
        }

        private void ParseBoard(string[] data)
        {
            int cartId = 0;

            for (int j = 0; j < this.height; j++)
            {
                for (var i = 0; i < this.width; i++)
                {
                    this.board[i + j * width] = data[j][i];

                    Direction dir;
                    if (cartToDirectionMap.TryGetValue(data[j][i], out dir))
                    {
                        this.carts.Add(new Cart()
                        {
                            ID = cartId++,
                            X = i,
                            Y = j,
                            Facing = dir,
                            Alive = true
                        });

                        // Remove cart from board.
                        if (dir == Direction.Left || dir == Direction.Right)
                        {
                            this.board[i + j * width] = '-';
                        }
                        else
                        {
                            this.board[i + j * width] = '|';
                        }
                    }
                }
            }
        }

        public Tuple<int, int> Tick()
        {
            Tuple<int, int> firstCollision = null;
            foreach (var cart in this.carts.OrderBy(c => c.X))
            {
                if (!cart.Alive)
                    continue;

                // Move the cart
                int nextX = cart.X + directionToOffsetMap[cart.Facing].Item1;
                int nextY = cart.Y + directionToOffsetMap[cart.Facing].Item2;
                cart.X = nextX;
                cart.Y = nextY;

                // Look for collision. If there are lots of carts (there aren't) we could switch this to 
                // track the cart on the board and just do cartToDirectionMap.TryGetValue(next, out ) == true to
                // determine collision. The downside of tracking the carts on the board is replacing the cart with the
                // previous piece, so we need to track that or potentially track the carts in a separate array.
                foreach (var testCart in this.carts.Where(tc => tc.ID != cart.ID && tc.Alive))
                {
                    if (cart.X == testCart.X && cart.Y == testCart.Y)
                    {
                        // Record first collision
                        if (firstCollision == null)
                            firstCollision = new Tuple<int, int>(cart.X, cart.Y);

                        // Mark carts dead.
                        cart.Alive = false;
                        testCart.Alive = false;
                        break;
                    }
                }

                // Update cart based on next part of path
                char nextPathItem = this.board[nextX + nextY * width];
                if (nextPathItem == '+')
                {
                    // Turn based on rules at intersections
                    cart.HandleIntersection();
                }
                else
                {
                    // Transition based on transition map for the current facing direction and type of path.
                    cart.Facing = transitionMap[cart.Facing][nextPathItem];
                }
            }

            return firstCollision;
        }
    }
}
