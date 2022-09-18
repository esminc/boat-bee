import { ModalView } from "@slack/bolt";
import { User } from "../model";

/**
 * ユーザプロフィールモーダル
 */
export const userProfileModal = (props: {
  callbackId: string;
  userName: string;
  user?: User;
  privateMetadata?: string;
}): ModalView => {
  return {
    type: "modal",
    callback_id: props.callbackId,
    private_metadata: props.privateMetadata,
    title: { type: "plain_text", text: "プロフィール" },
    submit: {
      type: "plain_text",
      text: props.user ? "更新" : "登録",
      emoji: true,
    },
    close: { type: "plain_text", text: "閉じる", emoji: true },
    blocks: [
      {
        type: "section",
        block_id: "section_user_name",
        text: {
          type: "plain_text",
          text: props.userName,
        },
      },
      {
        type: "input",
        block_id: "input_department",
        label: { type: "plain_text", text: "事業部" },
        element: {
          type: "static_select",
          action_id: "department_action",
          placeholder: {
            type: "plain_text",
            text: "事業部を選択してください",
            emoji: true,
          },
          // options: _make_options(user_department_dict),
        },
      },
      {
        type: "input",
        block_id: "input_job_type",
        label: { type: "plain_text", text: "主な仕事" },
        element: {
          type: "static_select",
          action_id: "job_type_action",
          placeholder: {
            type: "plain_text",
            text: "一番近いものを選択してください",
            emoji: true,
          },
          //options: _make_options(user_job_type_dict),
        },
      },
      {
        type: "input",
        block_id: "input_age_range",
        label: { type: "plain_text", text: "年齢層" },
        element: {
          type: "static_select",
          action_id: "age_range_action",
          placeholder: {
            type: "plain_text",
            text: "年齢層を選択してください",
            emoji: true,
          },
          //options: _make_options(user_age_range_dict),
        },
      },
    ],
  };
};
