from django.http import HttpResponse

import bricks.rpc
from codeschool import models
from codeschool.lms.listings.score_map import ScoreTable


class ScoreBoardMixin(models.RoutablePageMixin,
                      models.Page):
    """
    Basic ScoreBoard functionality.
    """

    class Meta:
        abstract = True

    def score_board(self, info=None):
        """
        Return a ScoreTable object with the grades of all students from the
        sub-page activities.
        """

        info = info or 'points'
        if info not in ['points', 'grade', 'stars', 'score']:
            raise ValueError('invalid info: %r' % info)

        board = ScoreTable(name=self.title)
        for page in self.get_children():
            col = page.specific.score_board(info=info)
            board.add_column(col)
        return board

    @bricks.rpc.route(r'^score-board/$')
    def serve_score_board(self, client):
        board = self.score_board()
        board.sort()
        board.add_total('total', method='sum')
        client.dialog(html=str(board))

    @models.route(r'^score-board[\.]csv/$')
    def serve_score_board_csv(self, request):
        board = self.score_board()
        board.sort()
        board.add_total('total', method='sum')
        return HttpResponse(board.to_csv())
