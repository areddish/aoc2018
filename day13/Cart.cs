namespace day13
{
    public class Cart
    {
        public int ID { get; set; }
        public Direction Facing { get; set; }
        public int X { get; set; }
        public int Y { get; set; }
        public bool Alive { get; set; }

        private Move nextMove = Move.Left;

        public void HandleIntersection()
        {
            var move = GetNextMove();

            if (move == Move.Straight)
            {
                return;
            }

            if (move == Move.Left)
            {
                switch (this.Facing)
                {
                    case Direction.Right:
                        Facing = Direction.Up;
                        break;
                    case Direction.Left:
                        Facing = Direction.Down;
                        break;
                    case Direction.Down:
                        Facing = Direction.Right;
                        break;
                    case Direction.Up:
                        Facing = Direction.Left;
                        break;
                }
            }
            else
            {
                switch (this.Facing)
                {
                    case Direction.Right:
                        Facing = Direction.Down;
                        break;
                    case Direction.Left:
                        Facing = Direction.Up;
                        break;
                    case Direction.Down:
                        Facing = Direction.Left;
                        break;
                    case Direction.Up:
                        Facing = Direction.Right;
                        break;
                }
            }
        }

        private Move GetNextMove()
        {
            var next = (int)this.nextMove;
            this.nextMove = (Move)((next + 1) % (int)Move.LIMIT);
            return (Move)next;
        }
    }
}
