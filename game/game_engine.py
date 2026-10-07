import pygame
from game.deck import Deck


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.deck = Deck()

        # Card state
        self.current_card = self.deck.draw()
        self.previous_card = None
        self.next_card = None

        # Game state
        self.score = 0
        self.streak = 0

        self.status_msg = "Will the next card be HIGHER or LOWER?"
        self.status_color = (220, 220, 220)

        # Reveal state
        self.reveal_active = False
        self.reveal_duration = 1000  # milliseconds
        self.reveal_until = 0

        # Buttons
        btn_w, btn_h = 140, 48

        self.btn_higher = pygame.Rect(
            width // 2 - btn_w - 20,
            height - 90,
            btn_w,
            btn_h,
        )

        self.btn_lower = pygame.Rect(
            width // 2 + 20,
            height - 90,
            btn_w,
            btn_h,
        )

        # Fonts
        self.font_title = pygame.font.SysFont(None, 40)
        self.font_medium = pygame.font.SysFont(None, 30)
        self.font_small = pygame.font.SysFont(None, 24)

    def evaluate_guess(self, guess):
        """Draw the next card and evaluate the player's prediction."""

        # Safety guard: do not allow another prediction during reveal.
        if self.reveal_active:
            return

        self.previous_card = self.current_card
        self.next_card = self.deck.draw()

        current_rank = self.current_card.numeric_rank
        next_rank = self.next_card.numeric_rank

        # ---------------------------------------------------------
        # TASK 3: PUSH / TIE
        # ---------------------------------------------------------
        if next_rank == current_rank:
            self.status_msg = (
                f"PUSH! {self.next_card.rank_str} vs "
                f"{self.current_card.rank_str}"
            )
            self.status_color = (245, 200, 80)

            # IMPORTANT:
            # Score is unchanged.
            # Streak is unchanged.

        # ---------------------------------------------------------
        # TASK 1 + TASK 2: HIGHER / LOWER + STREAK MULTIPLIER
        # ---------------------------------------------------------
        else:
            if guess == "HIGHER":
                correct = next_rank > current_rank
            else:
                correct = next_rank < current_rank

            if correct:
                self.streak += 1

                # 1st consecutive win = 1 point
                # 2nd consecutive win = 2 points
                # 3rd consecutive win = 3 points
                # etc.
                points_earned = self.streak

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

        # ---------------------------------------------------------
        # TASK 4: START SIDE-BY-SIDE REVEAL
        # ---------------------------------------------------------
        self.reveal_active = True
        self.reveal_until = (
            pygame.time.get_ticks() + self.reveal_duration
        )

    def handle_event(self, event):
        """Handle user input."""

        if event.type != pygame.MOUSEBUTTONDOWN:
            return

        if event.button != 1:
            return

        # Ignore clicks while the reveal is active.
        if self.reveal_active:
            return

        if self.btn_higher.collidepoint(event.pos):
            self.evaluate_guess("HIGHER")

        elif self.btn_lower.collidepoint(event.pos):
            self.evaluate_guess("LOWER")

    def update(self):
        """Advance the game after the reveal timer expires."""

        # Nothing to update if no reveal is active.
        if not self.reveal_active:
            return

        current_time = pygame.time.get_ticks()

        # Keep displaying both cards until the timer expires.
        if current_time < self.reveal_until:
            return

        # Reveal is finished.
        if self.next_card is not None:
            self.current_card = self.next_card

        self.previous_card = None
        self.next_card = None
        self.reveal_active = False
        self.reveal_until = 0

    def render(self, screen):
        """Render the complete game screen."""

        screen.fill((25, 80, 45))

        # ---------------------------------------------------------
        # TITLE
        # ---------------------------------------------------------
        title_surf = self.font_title.render(
            "High-Low Card Predictor",
            True,
            (245, 245, 245),
        )

        screen.blit(
            title_surf,
            (
                self.width // 2 - title_surf.get_width() // 2,
                25,
            ),
        )

        # ---------------------------------------------------------
        # SCORE
        # ---------------------------------------------------------
        score_surf = self.font_medium.render(
            f"Score: {self.score}",
            True,
            (255, 220, 80),
        )

        screen.blit(score_surf, (30, 30))

        # ---------------------------------------------------------
        # STREAK
        # ---------------------------------------------------------
        streak_surf = self.font_small.render(
            f"Streak: {self.streak}",
            True,
            (255, 255, 255),
        )

        screen.blit(streak_surf, (30, 65))

        # ---------------------------------------------------------
        # DECK
        # ---------------------------------------------------------
        rem_surf = self.font_small.render(
            f"Deck: {self.deck.remaining} left",
            True,
            (210, 210, 210),
        )

        screen.blit(
            rem_surf,
            (
                self.width - rem_surf.get_width() - 30,
                35,
            ),
        )

        # ---------------------------------------------------------
        # CARDS
        # ---------------------------------------------------------
        card_w, card_h = 120, 170

        if self.reveal_active:
            gap = 60

            total_width = (card_w * 2) + gap
            left_x = (self.width - total_width) // 2
            right_x = left_x + card_w + gap

            # Previous/current card
            self.previous_card.render(
                screen,
                left_x,
                100,
                card_w,
                card_h,
            )

            # Newly drawn card
            self.next_card.render(
                screen,
                right_x,
                100,
                card_w,
                card_h,
            )

            # VS
            vs_surf = self.font_small.render(
                "VS",
                True,
                (245, 245, 245),
            )

            screen.blit(
                vs_surf,
                (
                    self.width // 2 - vs_surf.get_width() // 2,
                    175,
                ),
            )

        else:
            # Normal state: only current card.
            self.current_card.render(
                screen,
                self.width // 2 - card_w // 2,
                100,
                card_w,
                card_h,
            )

        # ---------------------------------------------------------
        # STATUS MESSAGE
        # ---------------------------------------------------------
        status_surf = self.font_small.render(
            self.status_msg,
            True,
            self.status_color,
        )

        screen.blit(
            status_surf,
            (
                self.width // 2 - status_surf.get_width() // 2,
                300,
            ),
        )

        # ---------------------------------------------------------
        # BUTTONS
        # ---------------------------------------------------------
        buttons_enabled = not self.reveal_active

        if buttons_enabled:
            higher_color = (40, 140, 60)
            lower_color = (170, 50, 50)
        else:
            higher_color = (70, 90, 70)
            lower_color = (100, 70, 70)

        # HIGHER button
        pygame.draw.rect(
            screen,
            higher_color,
            self.btn_higher,
            border_radius=8,
        )

        pygame.draw.rect(
            screen,
            (220, 220, 220),
            self.btn_higher,
            width=2,
            border_radius=8,
        )

        high_surf = self.font_medium.render(
            "HIGHER",
            True,
            (255, 255, 255),
        )

        screen.blit(
            high_surf,
            (
                self.btn_higher.centerx - high_surf.get_width() // 2,
                self.btn_higher.centery - high_surf.get_height() // 2,
            ),
        )

        # LOWER button
        pygame.draw.rect(
            screen,
            lower_color,
            self.btn_lower,
            border_radius=8,
        )

        pygame.draw.rect(
            screen,
            (220, 220, 220),
            self.btn_lower,
            width=2,
            border_radius=8,
        )

        low_surf = self.font_medium.render(
            "LOWER",
            True,
            (255, 255, 255),
        )

        screen.blit(
            low_surf,
            (
                self.btn_lower.centerx - low_surf.get_width() // 2,
                self.btn_lower.centery - low_surf.get_height() // 2,
            ),
        )