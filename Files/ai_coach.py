class AICoach:

    def get_tip(self, snake, food, obstacles):
        head = snake.body[0]

        if head in obstacles.positions:
            return "Watch out! Avoid obstacles."

        x, y = head
        fx, fy = food.position

        if abs(x - fx) + abs(y - fy) < 5:
            return "Food is nearby. Go for it!"

        if len(snake.body) > 12:
            return "Your snake is getting long. Plan your turns."

        return "Collect food and stay alive!"