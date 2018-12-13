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
            else if (move == Move.Right)
            {
                int val = (int)Facing;
                val++;
                val %= (int)Direction.LIMIT;
                Facing = (Direction)val;
            }
            else
            {
                int val = (int)Facing;
                val--;
                if (val < 0)
                    val = (int)Direction.LIMIT - 1;
                Facing = (Direction)val;
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
