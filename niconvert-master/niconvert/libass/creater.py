from niconvert.libass.display import display_factory
from niconvert.libass.collision import Collision
from niconvert.libass.subtitle import Subtitle

class Creater:
    ''' 创建器 '''

    def __init__(self, config, danmakus):
        self.config = config
        self.danmakus = danmakus
        self.subtitles = self._subtitles()
        self.text = self._text()

    def _subtitles(self):
        collisions = {
            'scroll': Collision(self.config.line_count),
            'top': Collision(self.config.line_count),
            'bottom': Collision(self.config.line_count),
        }

        subtitles = []
        for danmaku in self.danmakus:

            # 丢弃不支持的
            if danmaku.style == 'none':
                continue

            # 创建显示方式对象
            display = display_factory(self.config, danmaku)
            collision = collisions[danmaku.style]
            line_index, waiting_offset = collision.detect(display)

            # 超过容忍的偏移量，丢弃掉此条弹幕
            if waiting_offset > self.config.drop_offset:
                continue

            # 接受偏移，更新碰撞信息
            display.relayout(line_index)
            collision.update(display.leave, line_index, waiting_offset)

            # 再加上自定义偏移
            offset = waiting_offset + self.config.custom_offset
            subtitle = Subtitle(danmaku, display, offset)

            subtitles.append(subtitle)
        return subtitles

    def _text(self):
        header = self.config.header_template.format(
            width=self.config.screen_width,
            height=self.config.screen_height,
            fontname=self.config.font_name,
            fontsize=self.config.base_font_size,
        )
        events = (subtitle.text for subtitle in self.subtitles)
        text = header + '\n'.join(events)
        return text
