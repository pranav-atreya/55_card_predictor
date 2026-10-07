import pygame
from game.deck import Deck

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.deck = Deck()

        self.current_card = self.deck.draw()
        self.next_card = None
        self.score = 0
        self.streak = 0
        self.status_msg = "Will the next card be HIGHER or LOWER?"
        self.status_color = (220, 220, 220)

        btn_w, btn_h = 140, 48
        self.btn_higher = pygame.Rect(width // 2 - btn_w - 20, height - 90, btn_w, btn_h)
        self.btn_lower = pygame.Rect(width // 2 + 20, height - 90, btn_w, btn_h)

        self.font_title = pygame.font.SysFont(None, 40)
        self.font_medium = pygame.font.SysFont(None, 30)
        self.font_small = pygame.font.SysFont(None, 24)

    def evaluate_guess(self, guess):
        """Draws next card and evaluates prediction."""
        self.next_card = self.deck.draw()

        current_rank = self.current_card.numeric_rank
        next_rank = self.next_card.numeric_rank

        # Same rank: PUSH. Score and streak remain unchanged.
        if next_rank == current_rank:
            self.status_msg = (
                f"PUSH! {self.next_card.rank_str} vs "
                f"{self.current_card.rank_str}"
            )
            self.status_color = (245, 200, 80)

        else:
            if guess == "HIGHER":
                correct = next_rank > current_rank
            else:
                correct = next_rank < current_rank

            if correct:
                self.streak += 1

                # Multiplier increases with each consecutive correct prediction.
                multiplier = self.streak
                points_earned = multiplier

                self.score += points_earned
                self.status_msg = (
                    f"CORRECT! +{points_earned} "
                    f"(Streak: {self.streak}x)"
                )
                self.status_color = (80, 220, 80)

            else:
                self.score = max(0, self.score - 1)
                self.streak = 0

                self.status_msg = (
                    f"WRONG! {self.next_card.rank_str} vs "
                    f"{self.current_card.rank_str}"
                )
                self.status_color = (235, 75, 75)

        self.current_card = self.next_card


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.btn_higher.collidepoint(event.pos):
                self.evaluate_guess("HIGHER")
            elif self.btn_lower.collidepoint(event.pos):
                self.evaluate_guess("LOWER")

    def update(self):
        pass

    def render(self, screen):
        screen.fill((25, 80, 45))

        title_surf = self.font_title.render("High-Low Card Predictor", True, (245, 245, 245))
        screen.blit(title_surf, (self.width // 2 - title_surf.get_width() // 2, 25))

        score_surf = self.font_medium.render(f"Score: {self.score}", True, (255, 220, 80))
        screen.blit(score_surf, (30, 30))

        streak_surf = self.font_small.render(
            f"Streak: {self.streak}",
            True,
            (255, 255, 255),
        )
        screen.blit(streak_surf, (30, 65))

        rem_surf = self.font_small.render(f"Deck: {self.deck.remaining} left", True, (210, 210, 210))
        screen.blit(rem_surf, (self.width - rem_surf.get_width() - 30, 35))

        card_w, card_h = 130, 180
        self.current_card.render(screen, self.width // 2 - card_w // 2, 100, card_w, card_h)

        status_surf = self.font_small.render(self.status_msg, True, self.status_color)
        screen.blit(status_surf, (self.width // 2 - status_surf.get_width() // 2, 310))

        pygame.draw.rect(screen, (40, 140, 60), self.btn_higher, border_radius=8)
        pygame.draw.rect(screen, (220, 220, 220), self.btn_higher, width=2, border_radius=8)
        high_surf = self.font_medium.render("HIGHER", True, (255, 255, 255))
        screen.blit(
            high_surf,
            (self.btn_higher.centerx - high_surf.get_width() // 2, self.btn_higher.centery - high_surf.get_height() // 2),
        )

        pygame.draw.rect(screen, (170, 50, 50), self.btn_lower, border_radius=8)
        pygame.draw.rect(screen, (220, 220, 220), self.btn_lower, width=2, border_radius=8)
        low_surf = self.font_medium.render("LOWER", True, (255, 255, 255))
        screen.blit(
            low_surf,
            (self.btn_lower.centerx - low_surf.get_width() // 2, self.btn_lower.centery - low_surf.get_height() // 2),
        )
